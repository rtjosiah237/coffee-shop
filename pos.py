from datetime import datetime

class PointOfSale:
    def __init__(self, db):
        self.db = db
    
    def sell_drink(self):
        print("\n----------------------------------------------")
        print("                  Sell Drinks                 ")
        print("----------------------------------------------")

        # Get the menu
        menu = self.db.run_query("SELECT name, price FROM Menu ORDER BY name")
        if not menu:
            print("No menu items available.")
            input("\nPress Enter to return  ")
            return

        # Display menu
        for idx, (name, price) in enumerate(menu, start=1):
            print(f"{idx}. {name} — ${price}")
        print("0. Finish order")

        # Collect order
        order = []
        while True:
            sel = input("\nSelect item # (0 to finish): ").strip()
            if sel == '0':
                break
            if not sel.isdigit() or not (1 <= int(sel) <= len(menu)):
                print("Invalid selection.")
                continue
            
            name, price = menu[int(sel) - 1]
            qty_str = input(f"Quantity for {name}: ").strip()
            if not qty_str.isdigit() or int(qty_str) <= 0:
                print("Invalid quantity.")
                continue
            
            order.append((name, int(qty_str), price))

        if not order:
            print("No items ordered.")
            input("\nPress Enter to return  ")
            return

        # Get payment method
        pm = input("Payment method (Cash/Credit Card/App): ").strip().title()
        if pm not in ("Cash", "Credit Card", "App"):
            print("Invalid payment method.")
            input("\nPress Enter to return  ")
            return

        # Create order ID and calculate total
        ts = datetime.now()
        total = sum(qty * price for _, qty, price in order)
        order_id = ts.strftime("%Y%m%d%H%M%S%f")

        try:
            self.db.begin()
            
            # Get current balance
            row = self.db.run_query(
                "SELECT balance FROM Accounting ORDER BY entry_date DESC LIMIT 1"
            )
            last_bal = row[0][0] if row else 0
            new_bal = last_bal + total

            # Update accounting
            self.db.run_query(
                "INSERT INTO Accounting(entry_date, balance) VALUES (:ts, :bal)",
                ts=ts, bal=new_bal
            )

            # Record sale
            self.db.run_query(
                "INSERT INTO Sales(order_id, order_time, payment_method, total) "
                "VALUES (:oid, :ts, :pm, :tot)",
                oid=order_id, ts=ts, pm=pm, tot=total
            )

            # Process each item in order
            for name, qty, price in order:
                line_tot = qty * price
                
                # Insert line item
                self.db.run_query(
                    "INSERT INTO LineItem(order_id, name, quantity, line_item_total) "
                    "VALUES (:oid, :n, :q, :lt)",
                    oid=order_id, n=name, q=qty, lt=line_tot
                )
                
                # Get ingredients for this drink
                ingreds = self.db.run_query(
                    "SELECT item_name, quantity FROM Ingredient WHERE name = :n",
                    n=name
                )
                
                # Reduce inventory for each ingredient
                for item, need in ingreds:
                    used = need * qty
                    
                    # Check if enough stock
                    quantity_in_stock = self.db.run_query(
                        "SELECT quantity_in_stock FROM Inventory WHERE item_name=:i", 
                        i=item
                    )
                    
                    if not quantity_in_stock or float(quantity_in_stock[0][0] - used) < 0:
                        raise ValueError(f"Not enough {item} in stock to fulfill order.")
                    
                    # Update inventory
                    self.db.run_query(
                        "UPDATE Inventory SET quantity_in_stock = quantity_in_stock - :u "
                        "WHERE item_name = :i",
                        u=used, i=item
                    )
            
            self.db.commit()
            print(f"\nOrder recorded successfully. Total: ${total:.2f}")
            
        except Exception as e:
            self.db.rollback()
            print(f"\nError processing order: {e}")
            input("\nPress Enter to return  ")
            return

        # Show preparation steps
        for name, qty, _ in order:
            steps = self.db.run_query(
                "SELECT step_number, step_name FROM PreparationStep "
                "WHERE name = :n ORDER BY step_number",
                n=name
            )
            if steps:
                print(f"\nPreparation for {name} (x{qty}):")
                for num, desc in steps:
                    print(f"  {num}. {desc}")

        input("\nPress Enter to return  ")