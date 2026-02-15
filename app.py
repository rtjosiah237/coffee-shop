import os
import sys
import time
from database import Database
from employee_manager import EmployeeManager
from schedule_manager import ScheduleManager
import config


class CoffeeShopApp:
    def __init__(self):
        self.db = None
        self.employee_manager = None
        self.schedule_manager = None
        self.curr_user = None
        self.curr_role = None
        self.curr_name = None
        self.main()

    def connect_db(self):
        try:
            self.db = Database(
                user=config.USER,
                database=config.DATABASE,
                password=config.PASSWORD,
                host=config.HOST,
                port=config.PORT
            )
            self.db.connect()
            
            self.employee_manager = EmployeeManager(self.db)
            self.schedule_manager = ScheduleManager(self.db)
            
        except Exception as e:
            print(f"Error connecting to database: {e}")
            sys.exit(1)

    def login(self):
        os.system('clear')
        print("\n----------------------------------------------")
        print("       Login to the Coffeeshop App")
        print("----------------------------------------------")
        print("""
             (  )   (   )  )
            ) (   )  (  (
            ( )  (    ) )
             _____________
            <_____________> ___
            |             |/ _ \\
            |             | | |
            |             |_| |
         ___|             |\\___/
         /    \\___________/    \\
        \\_____________________/
        """)
        print("----------------------------------------------")

        username = input("Username: ").strip()
        password = input("Password: ").strip()

        if username in config.USERS:
            if password == config.USERS[username]["password"]:
                self.curr_user = username
                self.curr_role = config.USERS[username]["role"]
                self.curr_name = config.USERS[username]["name"]
                print("\n----------------------------------------------")
                print(f"Welcome back, {self.curr_name}!")
                time.sleep(1)
                return True
            else:
                print("Invalid Password. Please try again.")
                return False
        else:
            print("Invalid Username. Please try again.")
            return False

    def manager_menu(self):
        logout = False
        while not logout:
            os.system('clear')
            print("           Coffee Shop Manager Menu           ")
            print("==============================================")
            print("1. Employee Management")
            print("2. Barista Schedule Management")
            print("3. Inventory Management (Coming Soon)")
            print("4. Accounting (Coming Soon)")
            print("5. Analytics (Coming Soon)")
            print("6. Logout")
            print("==============================================")

            option = input("Select an option: ").strip()

            if option == '1':
                self.employee_management_menu()
            elif option == '2':
                self.barista_schedule_menu()
            elif option == '3':
                print("Inventory management coming soon...")
                time.sleep(1)
            elif option == '4':
                print("Accounting coming soon...")
                time.sleep(1)
            elif option == '5':
                print("Analytics coming soon...")
                time.sleep(1)
            elif option == '6':
                logout = True
            else:
                print("Invalid option. Please try again.")
                time.sleep(1)

    def employee_management_menu(self):
        exit_menu = False
        while not exit_menu:
            os.system('clear')
            print("           Employee Management Menu           ")
            print("==============================================")
            print("a. Add New Employee")
            print("b. Edit Existing Employee")
            print("c. Delete Employee")
            print("d. Exit")
            print("==============================================")

            option = input("Select an option: ").strip().lower()

            if option == 'a':
                self.employee_manager.add_employees()
                input("\nPress Enter to continue...")
            elif option == 'b':
                self.employee_manager.edit_employees()
                input("\nPress Enter to continue...")
            elif option == 'c':
                self.employee_manager.delete_employees()
                input("\nPress Enter to continue...")
            elif option == 'd':
                exit_menu = True
            else:
                print("Invalid option. Please try again.")
                time.sleep(1)

    def barista_schedule_menu(self):
        exit_menu = False
        while not exit_menu:
            os.system('clear')
            print("       Barista Schedule Menu       ")
            print("===================================")
            print("a. View Schedule")
            print("b. Add Shift")
            print("c. Edit Shift")
            print("d. Delete Shift")
            print("e. Exit")
            print("===================================")
            
            option = input("Select an option: ").strip().lower()

            if option == 'a':
                self.schedule_manager.view_barista_schedule()
                input("\nPress Enter to continue...")
            elif option == 'b':
                self.schedule_manager.add_barista_shift()
                input("\nPress Enter to continue...")
            elif option == 'c':
                self.schedule_manager.edit_barista_shift()
                input("\nPress Enter to continue...")
            elif option == 'd':
                self.schedule_manager.delete_barista_shift()
                input("\nPress Enter to continue...")
            elif option == 'e':
                exit_menu = True
            else:
                print("Invalid option. Please try again.")
                time.sleep(1)

    def main(self):
        # Login loop
        while True:
            if self.login():
                break
            user_choice = input("\nDo you want to try again? (yes/no): ").strip().lower()
            if user_choice != "yes":
                print("Goodbye!")
                sys.exit(0)

        # Connect to database
        self.connect_db()
        
        os.system('clear')

        # Route to appropriate menu based on role
        if 'manager' in self.curr_role:
            self.manager_menu()
        elif 'barista' in self.curr_role:
            print("Barista menu coming soon...")
            time.sleep(2)
        
        # Close database connection
        self.db.close()
        print("\nLogged out successfully. Goodbye!")


if __name__ == "__main__":
    app = CoffeeShopApp()


