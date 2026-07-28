
from exceptions import *
from database import Database
from utils import *


db = Database()
current_customer = None



# Start


def start():

    while True:

        print("\n==============================")
        print(" BANK MANAGEMENT SYSTEM ")
        print("=====================================")
        print("1. Login")
        print("2. Exit")

        ch = input("\nEnter Choice : ")

        if ch == "1":

            login()

        elif ch == "2":

            db.close()

            print("\nThank You")

            break

        else:

            print("\nInvalid Choice")



# Login


def login():

    print("\n========== LOGIN ==========")

    print("1. Manager")
    print("2. Employee")
    print("3. Customer")

    role = input("\nSelect Role : ")

    user = input("Username : ")

    pwd = input("Password : ")

    if role == "1":

        row = db.login("Manager", user, pwd)

        if row:

            manager()

        else:

            print("\nInvalid Login")

    elif role == "2":

        row = db.login("Employee", user, pwd)

        if row:

            employee()

        else:

            print("\nInvalid Login")


    elif role == "3":

        global current_customer

        row = db.login("Customer", user, pwd)

        if row:

            current_customer = row

            customer()


        else:

            print("\nInvalid Login")

# Manager Menu


def manager():

    while True:

        print("\n========== MANAGER ==========")
        print("1. Add Employee")
        print("2. View Employee")
        print("3. Search Employee")
        print("4. Update Employee")
        print("5. Delete Employee")
        print("6. Logout")

        ch = input("\nEnter Choice : ")

        if ch == "1":

            name = input("Name : ")

            phone = input("Phone : ")
            user = input("Username : ")
            pwd = input("Password : ")

            try:
                if not validphone(phone):
                    raise InvalidPhoneError()

            except InvalidPhoneError as e:
                print(e)
                continue
            try:
                if not validuser(user):
                    raise InvalidUsernameError()

            except InvalidUsernameError as e:
                print(e)
                continue
            try:
                if not validpwd(pwd):
                    raise InvalidPasswordError()

            except InvalidPasswordError as e:
                print(e)
                continue

            db.addemployee(

                name,
                phone,
                user,
                pwd
            )

            print("\nEmployee Added")

        elif ch == "2":

            rows = db.getemployee()

            print()

            print("-" * 90)
            print("ID-----------------------NAME--------------------PHONE--------------------USERNAME")
            print("-" * 90)

            for row in rows:

                print(
                    row.EmployeeID,
                    "\t",
                    row.Name,
                    "\t",
                    row.Phone,
                    "\t",
                    row.Username
                )

        elif ch == "3":

            name = input("Enter Name : ")

            rows = db.searchemployee(name)

            if not rows:
                print("\nEmployee not found.")
            else:
                print("\n========== EMPLOYEE DETAILS ==========")
                for row in rows:
                    print(f"""
            Employee ID : {row.EmployeeID}
            Name        : {row.Name}
            Phone       : {row.Phone}
            Username    : {row.Username}
            """)

        elif ch == "4":

            empid = input("Employee ID : ")
            name = input("Name : ")
            phone = int(input("Phone : "))
            user = input("Username : ")

            db.updateemployee(
                empid,
                name,
                phone,
                user
            )

            print("\nEmployee Updated")

        elif ch == "5":

            empid = input("Employee ID : ")

            db.deleteemployee(empid)

            print("\nEmployee Deleted")

        elif ch == "6":

            break

        else:

            print("\nInvalid Choice")



# Employee Menu

def employee():

    while True:

        print("\n========== EMPLOYEE ==========")
        print("1. Customer Details")
        print("2. Add Customer")
        print("3. Open Account")
        print("4. Deposit")
        print("5. Withdraw")
        print("6. Transfer")
        print("7. Logout")

        ch = input("\nEnter Choice : ")


        # Customer Details


        if ch == "1":

            custid = input("Customer ID : ")

            rows = db.getcustomerdetails(custid)

            if len(rows) == 0:

                print("\nCustomer Not Found")
                continue

            print("\n========== ============CUSTOMER =======================")
            print("ID      :", rows[0].CustomerID)
            print("Name    :", rows[0].Name)
            print("Phone   :", rows[0].Phone)
            print("Address :", rows[0].Address)
            print("User    :", rows[0].Username)

            print("\nAccounts")
            print("----------------------------------------------------------------")

            for row in rows:

                if row.AccountNumber:

                    print(
                        row.AccountNumber,
                        "Balance :",
                        row.Balance
                    )

            print("\nTransactions")
            print("--------------------------------")

            trans = db.getcustomertrans(custid)

            if len(trans) == 0:

                print("No Transaction")

            else:

                for row in trans:

                    print(
                        row.TransactionID,
                        row.AccountNumber,
                        row.TransactionType,
                        row.Amount,
                        row.TransactionDate
                    )


        # Add Customer


        elif ch == "2":


            name = input("Name : ")
            phone = input("Phone : ")
            address = input("Address : ")
            user = input("Username : ")
            pwd = input("Password : ")
            try:
                if not validphone(phone):
                    raise InvalidPhoneError()

            except InvalidPhoneError as e:
                print(e)
                continue
            try:
                if not validuser(user):
                    raise InvalidUsernameError()

            except InvalidUsernameError as e:
                print(e)
                continue

            try:
                if not validpwd(pwd):
                    raise InvalidPasswordError()

            except InvalidPasswordError as e:
                print(e)
                continue

            customerid = db.addcustomer(
                name,
                phone,
                address,
                user,
                pwd
            )

            print("\nCustomer Added Successfully")
            print("Customer ID :", customerid)

        # Open Account

        elif ch == "3":

            custid = input("Customer ID : ")

            rows = db.getcustomerdetails(custid)

            if len(rows) == 0:
                print("\nCustomer Not Found")

                continue

            while True:

                no = genaccno()

                if db.checkaccount(no) is None:
                    break

            acctype = input("Account Type (Saving/Current) : ")

            bal = float(input("Opening Balance : "))

            if bal < 1000:
                print("\nMinimum Balance is 1000")

                continue

            db.openaccount(
                custid,
                no,
                acctype,
                bal
            )

            print("\nAccount Created Successfully")
            print("Account Number :", no)



        # Deposit


        elif ch == "4":

            custid = input("Customer ID : ")

            rows = db.getaccountbycust(custid)

            if len(rows) == 0:

                print("No Account")

                continue

            print()

            for i, row in enumerate(rows, start=1):

                print(i, row.AccountNumber, row.Balance)

            no = int(input("\nSelect Account : "))

            acc = rows[no - 1].AccountNumber

            amt = float(input("Amount : "))

            db.deposit(acc, amt)

            print("\nDeposit Successful")


        # Withdraw


        elif ch == "5":

            custid = input("Customer ID : ")

            rows = db.getaccountbycust(custid)

            if len(rows) == 0:

                print("No Account")

                continue

            print()

            for i, row in enumerate(rows, start=1):

                print(i, row.AccountNumber, row.Balance)

            no = int(input("\nSelect Account : "))

            acc = rows[no - 1].AccountNumber

            amt = float(input("Amount : "))

            db.withdraw(acc, amt)

            print("\nWithdraw Successful")


        # Transfer

        elif ch == "6":


            custid = input("Customer ID : ")

            rows = db.getaccountbycust(custid)

            if len(rows) == 0:

                print("No Account")

                continue

            print()

            for i, row in enumerate(rows, start=1):

                print(i, row.AccountNumber)

            no = int(input("\nSelect Account : "))

            sendacc = rows[no - 1].AccountNumber

            recvacc = input("Receiver Account No : ")


            amt = float(input("Amount : "))

            if amt <= 0:
                print("\nInvalid Amount")

                continue

            bal = db.getbalance(sendacc)

            if amt > bal:
                print("\nInsufficient Balance")

                continue

            if db.getbalance(recvacc) is None:
                print("\nReceiver Account Not Found")

                continue

            db.transfer(sendacc, recvacc, amt)

            db.addtransaction(sendacc, "Transfer", amt)



            print("\nTransfer Successful")

        # ==========================
        # Logout
        # ==========================

        elif ch == "7":

            break

        else:

            print("\nInvalid Choice")


# ==========================
# Customer Menu
# ==========================

def customer():

    while True:

        print("\n========== CUSTOMER ==========")
        print("1. my account")
        print("2. check balance")

        print("3. deposit")
        print("4. withdrow")
        print("5. mini statement")
        print("6. log out")


        ch = input("\nEnter Choice : ")

        # My Accounts


        if ch == "1":

            rows = db.getcustomerdetails(current_customer.CustomerID)
            if rows:
                row = rows[0]

                print("\n========== MY PROFILE ==========")

                print(f"""
            Customer ID    : {row.CustomerID}
            Name           : {row.Name}
            Phone          : {row.Phone}
            Address        : {row.Address}
            Username       : {row.Username}

            Account Number : {row.AccountNumber}
           
            Balance        : ₹{row.Balance}
           
            """)

        elif ch == "2":

            rows = db.getaccountbycust(current_customer.CustomerID)

            if len(rows) == 0:
                print("\nNo Account Found")

                continue

            print()

            for i, row in enumerate(rows, start=1):
                print(i, row.AccountNumber, row.Balance)

            no = int(input("\nSelect Account : "))

            acc = rows[no - 1].AccountNumber

            bal = db.getbalance(acc)

            print("\nBalance :", bal)


        elif ch == "3":



            rows = db.getaccountbycust(current_customer.CustomerID)

            if len(rows) == 0:
                print("\nNo Account Found")

                continue

            print()

            for i, row in enumerate(rows, start=1):
                print(i, row.AccountNumber, row.Balance)

            no = int(input("\nSelect Account : "))

            acc = rows[no - 1].AccountNumber

            amt = float(input("Amount : "))

            if amt <= 0:
                print("\nInvalid Amount")

                continue

            db.deposit(acc, amt)

            print("\nDeposit Successful")

        elif ch == "4":



            rows = db.getaccountbycust(current_customer.CustomerID)

            if len(rows) == 0:
                print("\nNo Account Found")

                continue

            print()

            for i, row in enumerate(rows, start=1):
                print(i, row.AccountNumber, row.Balance)

            no = int(input("\nSelect Account : "))

            acc = rows[no - 1].AccountNumber

            amt = float(input("Amount : "))

            if amt <= 0:
                print("\nInvalid Amount")

                continue

            bal = db.getbalance(acc)

            if amt > bal:
                print("\nInsufficient Balance")

                continue

            db.withdraw(acc, amt)

            print("\nWithdraw Successful")
        elif ch == "5":

            rows = db.getaccountbycust(current_customer.CustomerID)

            if len(rows) == 0:
                print("\nNo Account Found")

                continue

            print()

            for i, row in enumerate(rows, start=1):
                print(i, row.AccountNumber)

            try:
                no = int(input("\nSelect Account : "))

                if no < 1 or no > len(rows):
                    print("\nInvalid Account Selection")
                    continue

            except ValueError:
                print("\nPlease enter a valid number.")
                continue

            acc = rows[no - 1].AccountNumber



            rows = db.gettransaction(acc)

            if len(rows) == 0:

                print("\nNo Transaction Found")

            else:

                print("\n========== MINI STATEMENT ==========")

                for row in rows:
                    print(
                        row.TransactionID,
                        acc,
                        row.TransactionType,
                        row.Amount,
                        row.TransactionDate
                    )

        elif ch == "6":

            break

