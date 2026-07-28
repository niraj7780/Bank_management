"""
=========================================
File : database.py
Purpose : Database Functions
=========================================
"""
import hashlib
import pyodbc
from config import *


class Database:

    # Connect Database
    def __init__(self):

        self.conn = pyodbc.connect(
            f"DRIVER={driver};"
            f"SERVER={server};"
            f"DATABASE={database};"
            "Trusted_Connection=yes;"
        )

        self.cur = self.conn.cursor()
        self.cur.execute("SELECT DB_NAME()")
        print(self.cur.fetchone()[0])

    # ---------------------------
    # Login
    # ---------------------------
    def login(self, table, user, pwd):

        pwd = self.hash_password(pwd)

        sql = f"""
        SELECT *
        FROM {table}
        WHERE Username=?
        AND Password=?
        """

        self.cur.execute(sql, (user, pwd))

        return self.cur.fetchone()

    # ---------------------------
    # Manager
    # ---------------------------

    def addmanager(self, name, phone, user, pwd):

        pwd = self.hash_password(pwd)

        sql = """
        INSERT INTO Manager
        (
            Name,
            Phone,
            Username,
            Password
        )
        OUTPUT INSERTED.ManagerID
        VALUES (?, ?, ?, ?)
        """

        self.cur.execute(sql, (name, phone, user, pwd))

        managerid = self.cur.fetchone()[0]

        self.conn.commit()

        return managerid
    # ---------------------------
    # Employee
    # ---------------------------
    def addemployee(self, name, phone, user, pwd):

        pwd = self.hash_password(pwd)

        sql = """
        INSERT INTO Employee
        (
            Name,
            Phone,
            Username,
            Password
        )
        OUTPUT INSERTED.EmployeeID
        VALUES
        (
            ?, ?, ?, ?
        )
        """

        self.cur.execute(
            sql,
            (name, phone, user, pwd)
        )

        employeeid = self.cur.fetchone()[0]

        self.conn.commit()

        return employeeid

    def getemployee(self):

        self.cur.execute("EXEC EmployeeReport")

        return self.cur.fetchall()

    def searchemployee(self, name):

        sql = """
        SELECT *
        FROM Employee
        WHERE Name LIKE ?
        """

        self.cur.execute(
            sql,
            ("%" + name + "%",)
        )

        return self.cur.fetchall()

    def updateemployee(self, empid, name, phone, user):

        sql = """
        UPDATE Employee
        SET
            Name=?,
            Phone=?,
            Username=?
        WHERE EmployeeID=?
        """

        self.cur.execute(
            sql,
            (name, phone, user, empid)
        )

        self.conn.commit()

    def deleteemployee(self, empid):

        self.cur.execute(
            """
            DELETE FROM Employee
            WHERE EmployeeID=?
            """,
            (empid,)
        )

        self.conn.commit()

    # ---------------------------
    # Customer
    # ---------------------------
    def addcustomer(self, name, phone, address, username, password):

        password = self.hash_password(password)

        sql = """
        INSERT INTO Customer
        (
            Name,
            Phone,
            Address,
            Username,
            Password
        )
        OUTPUT INSERTED.CustomerID
        VALUES
        (
            ?, ?, ?, ?, ?
        )
        """

        self.cur.execute(
            sql,
            (name, phone, address, username, password)
        )

        customerid = self.cur.fetchone()[0]

        self.conn.commit()

        return customerid

    def getcustomer(self):

        self.cur.execute("EXEC CustomerReport")

        return self.cur.fetchall()
    # Show customer details
    def getcustomerdetails(self, custid):

        self.cur.execute(
            "EXEC CustomerDetails ?",
            (custid,)
        )

        return self.cur.fetchall()





    # Account

    def openaccount(self, custid, accno, acctype, bal):
        sql = """
        INSERT INTO Account
        (
            CustomerID,
            AccountNumber,
            Balance,
            AccountType
        )
        VALUES
        (
            ?, ?, ?, ?
        )
        """

        self.cur.execute(
            sql,
            (custid, accno, bal, acctype)
        )

        self.conn.commit()





    def getaccount(self):

        self.cur.execute(
            """
            SELECT *
            FROM Account
            ORDER BY AccountID
            """
        )

        return self.cur.fetchall()

    # Check account number
    def checkaccount(self, accno):
        sql = """
        SELECT *
        FROM Account
        WHERE AccountNumber = ?
        """

        self.cur.execute(sql, (accno,))

        return self.cur.fetchone()

    def getbalance(self, accno):

        self.cur.execute(
            """
            SELECT Balance
            FROM Account
            WHERE AccountNumber=?
            """,
            (accno,)
        )

        row = self.cur.fetchone()

        if row:

            return row.Balance

        return None

    # ---------------------------
    # Deposit
    # ---------------------------

    def deposit(self, accno, amt):
        self.cur.execute(
            "EXEC DepositMoney ?, ?",
            (accno, amt)
        )
        self.conn.commit()

    # ---------------------------
    # Withdraw
    # ---------------------------

    def withdraw(self, accno, amt):
        self.cur.execute(
            "EXEC WithdrawMoney ?, ?",
            (accno, amt)
        )
        self.conn.commit()

    # ---------------------------
    # Transfer
    # ---------------------------
    def transfer(self, sendacc, recvacc, amt):

        try:

            self.cur.execute(
                """
                UPDATE Account
                SET Balance = Balance - ?
                WHERE AccountNumber = ?
                """,
                (amt, sendacc)
            )

            self.cur.execute(
                """
                UPDATE Account
                SET Balance = Balance + ?
                WHERE AccountNumber = ?
                """,
                (amt, recvacc)
            )

            self.conn.commit()

        except:

            self.conn.rollback()


    # ---------------------------
    # Transaction
    # ---------------------------

    def addtransaction(self, accno, transtype, amt):
        sql = """
        INSERT INTO [Transaction]
        (
            AccountNumber,
            TransactionType,
            Amount
        )
        VALUES
        (
            ?, ?, ?
        )
        """

        self.cur.execute(
            sql,
            (accno, transtype, amt)
        )

        self.conn.commit()

    def gettransaction(self, accno):

        self.cur.execute(
            "EXEC MiniStatement ?",
            (accno,)
        )

        return self.cur.fetchall()



    # Show customer transactions
    def getcustomertrans(self, custid):
        sql = """
        SELECT
            t.TransactionID,
            t.AccountNumber,
            t.TransactionType,
            t.Amount,
            t.TransactionDate
        FROM [Transaction] t
        JOIN Account a
        ON t.AccountNumber = a.AccountNumber
        WHERE a.CustomerID = ?
        ORDER BY t.TransactionDate DESC
        """

        self.cur.execute(sql, (custid,))

        return self.cur.fetchall()

    # Show accounts of customer
    def getaccountbycust(self, custid):
        sql = """
        SELECT
            AccountNumber,
            Balance
        FROM Account
        WHERE CustomerID = ?
        """

        self.cur.execute(sql, (custid,))

        return self.cur.fetchall()

    # ---------------------------
    # Close
    # ---------------------------

    def close(self):

        self.cur.close()

        self.conn.close()

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def checkusername(self, table, username):

        sql = f"""
        SELECT 1
        FROM {table}
        WHERE Username = ?
        """

        self.cur.execute(sql, (username,))

        return self.cur.fetchone()
