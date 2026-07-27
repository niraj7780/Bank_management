"""
=========================================
File : menu.py
Purpose : CLI Menu
=========================================
"""

from database import Database
from utils import *

db = Database()



# Start


def start():

    while True:

        print("\n==============================")
        print(" BANK MANAGEMENT SYSTEM ")
        print("==============================")
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

        row = db.login("Customer", user, pwd)

        if row:

            customer()

        else:

            print("\nInvalid Login")

    else:

        print("\nInvalid Choice")



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

            if not validphone(phone):

                print("Invalid Phone")
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

            print("-" * 70)
            print("ID\tNAME\tPHONE\tUSERNAME")
            print("-" * 70)

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

            print()

            for row in rows:

                print(
                    row.EmployeeID,
                    row.Name,
                    row.Phone,
                    row.Username
                )

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

        # ==========================
        # Customer Details
        # ==========================

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
            if not validphone(phone):
                print("\nInvalid Phone")

                continue

            if not validuser(user):
                print("\nInvalid Username")

                continue

            if not validpwd(pwd):
                print("\nInvalid Password")

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

            db.addtransaction(acc, "Deposit", amt)

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

            db.addtransaction(acc, "Withdraw", amt)

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

            custid = input("Customer ID : ")

            rows = db.getaccountbycust(custid)

            if len(rows) == 0:
                print("\nNo Account Found")

                continue

            print("\n========== MY ACCOUNTS ==========")
            print("ACCOUNT NO\t\tBALANCE")
            print("----------------------------------------")

            for row in rows:
                print(
                    row.AccountNumber,
                    "\t",
                    row.Balance
                )

        if ch == "2":

            accno1 = input("Account No : ")

            bal = db.getbalance(accno1)

            print("\nBalance :", bal)


        elif ch == "3":

            custid = input("Customer ID : ")

            rows = db.getaccountbycust(custid)

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

            db.addtransaction(acc, "Deposit", amt)

            print("\nDeposit Successful")

        elif ch == "4":

            custid = input("Customer ID : ")

            rows = db.getaccountbycust(custid)

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

            db.addtransaction(acc, "Withdraw", amt)

            print("\nWithdraw Successful")
        elif ch == "5":

            acc = input("Account No : ")

            rows = db.gettransaction(acc)

            if len(rows) == 0:

                print("\nNo Transaction Found")

            else:

                print("\n========== MINI STATEMENT ==========")

                for row in rows:
                    print(
                        row.TransactionID,
                        row.AccountNumber,
                        row.TransactionType,
                        row.Amount,
                        row.TransactionDate
                    )

        elif ch == "6":

            break

        else:

            print("\nInvalid Choice")