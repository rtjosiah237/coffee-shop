class EmployeeManager:
    def __init__(self, db):
        self.db = db
    
    def add_employees(self):
        print("\n----------------------------------------------")
        print("            Add a New Employee")
        print("----------------------------------------------")
        print("Please enter the following details: \n")
        try:
            new_user_name = input("Enter Employee Name: ").title().strip()
            if not new_user_name:
                raise ValueError("Employee name cannot be empty.")

            new_user_ssn = input("Enter Employee Social Security Number (Please Provide SSN in XXX-XX-XXXX format): ").strip()
            if not new_user_ssn:
                raise ValueError("Employee SSN cannot be empty.")

            new_user_email = input("Enter Employee Email: ").strip()
            if not new_user_email:
                raise ValueError("Employee Email cannot be empty.")

            new_user_salary = input("Enter Employee Salary: $")
            try:
                new_user_salary = float(new_user_salary)
                if new_user_salary < 0:
                    raise ValueError("Invalid Salary Value.")
            except ValueError as e:
                raise ValueError("Invalid salary format. Please provide a valid number.")

            new_user_role = input("Enter Employee Role (Barista/Manager/Both): ").lower().strip()
            if not new_user_role:
                raise ValueError("Employee Role cannot be empty.")

            add_query = """
            INSERT INTO employee (SSN, name, email, salary)
            VALUES (:ssn, :name, :email, :salary)
            """

            new_employee = {
                "ssn": new_user_ssn,
                "name": new_user_name,
                "email": new_user_email,
                "salary": new_user_salary
            }

            self.db.begin()
            self.db.run_query(add_query, **new_employee)

            if new_user_role == "barista" or new_user_role == "both":
                barista_query = """
                INSERT INTO barista (SSN) 
                VALUES (:ssn)
                """
                self.db.run_query(barista_query, ssn=new_user_ssn)

            if new_user_role == "manager" or new_user_role == "both":
                ownership_percentage = input("Enter ownership percentage (Between 0 to 100): ")
                try:
                    ownership_percentage = float(ownership_percentage)
                    if not 0 <= ownership_percentage <= 100:
                        raise ValueError("Ownership percentage must be between 0 and 100")
                except ValueError as e:
                    raise ValueError("Invalid ownership percentage; please enter a valid number")

                manager_query = """
                INSERT INTO manager (SSN, ownership_percentage) 
                VALUES (:ssn, :ownership_percentage)
                """
                self.db.run_query(manager_query, ssn=new_user_ssn, ownership_percentage=ownership_percentage)

            self.db.commit()
            print(f"{new_user_name} was successfully added to employees!")

        except Exception as e:
            self.db.rollback()
            print(f"Error occurred: {e}")
    
    def delete_employees(self):
        print("\n----------------------------------------------")
        print("            Delete Existing Employee")
        print("----------------------------------------------")
        print("Please enter the following details: \n")

        try:
            employee_name = input("Enter Employee Name: ").title().strip()
            if not employee_name:
                raise ValueError("Employee name cannot be empty.")

            employee_ssn = input("Enter Employee Social Security Number (Please Provide SSN in XXX-XX-XXXX format): ").strip()
            if not employee_ssn:
                raise ValueError("Employee SSN cannot be empty.")

            if input(f"Are you sure you want to delete {employee_name}? (Yes/No): ").lower() == 'no':
                return
            else:
                self.db.begin()
                name_check = self.db.run_query("SELECT name FROM employee WHERE SSN = :ssn", ssn=employee_ssn)
                if name_check != employee_name:
                    raise ValueError("No employee found with this SSN.")

                ssn_check = self.db.run_query("SELECT SSN FROM employee WHERE name = :name", name=employee_name)
                if ssn_check != employee_ssn:
                    raise ValueError("Error finding employee.")

                self.db.run_query("DELETE FROM Barista_Schedule WHERE barista_SSN = :ssn", ssn=employee_ssn)
                self.db.run_query("DELETE FROM Manager WHERE SSN = :ssn", ssn=employee_ssn)
                self.db.run_query("DELETE FROM Barista WHERE SSN = :ssn", ssn=employee_ssn)
                self.db.run_query("DELETE FROM Employee WHERE SSN = :ssn", ssn=employee_ssn)
                self.db.commit()
                print(f"Employee {employee_name} has been successfully deleted.")

        except Exception as e:
            self.db.rollback()
            print(f"An error occurred when deleting employee.")
    
    def edit_employees(self):
        print("\n----------------------------------------------")
        print("            Edit Existing Employee")
        print("----------------------------------------------")
        print("Please enter the following details: \n")
        try:
            employee_name = input("Enter Employee Name: ").title().strip()
            if not employee_name:
                raise ValueError("Employee name cannot be empty.")

            employee_ssn = input("Enter Employee Social Security Number (Please Provide SSN in XXX-XX-XXXX format): ").strip()
            if not employee_ssn:
                raise ValueError("Employee SSN cannot be empty.")

            self.db.begin()

            print("\n----------------------------------------------")
            print("a. Edit Employee Salary")
            print("b. Edit Employee Email Address")
            print("----------------------------------------------")

            option = input("\nSelect an option: ").strip().lower()
            if option == 'a':
                new_salary = float(input("Enter New Salary Amount: $"))
                salary_query = """
                UPDATE Employee 
                SET salary = :salary
                WHERE SSN = :ssn AND name = :name
                """

                self.db.run_query(salary_query, salary=new_salary, ssn=employee_ssn, name=employee_name)
                self.db.commit()
                print(f"Employee {employee_name} salary has been updated to {new_salary}.")
            elif option == 'b':
                new_email = (input("Enter New Email Address: ")).strip()
                email_query = """
                UPDATE Employee 
                SET email = :email
                WHERE SSN = :ssn AND name = :name
                """

                self.db.run_query(email_query, email=new_email, ssn=employee_ssn, name=employee_name)
                self.db.commit()
                print(f"Employee {employee_name} email has been updated to {new_email}.")
            else:
                print("Invalid option. Please try again.")

        except Exception as e:
            self.db.rollback()
            print("Error.")