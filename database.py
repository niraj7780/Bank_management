"""
=========================================
File : database.py
Purpose : Database Functions
=========================================
"""

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

        sql = f"""
        SELECT *
        FROM {table}
        WHERE Username=?
        AND Password=?
        """

        self.cur.execute(sql, (user, pwd))

        return self.cur.fetchone()

    # ---------------------------
    # Employee
    # ---------------------------

    def addemployee(self, mgrid, name, phone, user, pwd):

        sql = """
        INSERT INTO Employee
        (
            ManagerID,
            Name,
            Phone,
            Username,
            Password
        )
        VALUES
        (
            ?, ?, ?, ?, ?
        )
        """

        self.cur.execute(
            sql,
            (mgrid, name, phone, user, pwd)
        )

        self.conn.commit()

    def getemployee(self):

        self.cur.execute(
            """
            SELECT *
            FROM Employee
            ORDER BY EmployeeID
            """
        )

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

    def addcustomer(self, empid, name, phone, address, user, pwd):

        sql = """
        INSERT INTO Customer
        (
            EmployeeID,
            Name,
            Phone,
            Address,
            Username,
            Password
        )
        VALUES
        (
            ?, ?, ?, ?, ?, ?
        )
        """

        self.cur.execute(
            sql,
            (empid, name, phone, address, user, pwd)
        )

        self.conn.commit()

    def getcustomer(self):

        self.cur.execute(
            """
            SELECT *
            FROM Customer
            ORDER BY CustomerID
            """
        )

        return self.cur.fetchall()

    # Show customer details
    def getcustomerdetails(self, custid):
        sql = """
        SELECT
            c.CustomerID,
            c.Name,
            c.Phone,
            c.Address,
            c.Username,
            a.AccountNumber,
            a.Balance
        FROM Customer c
        LEFT JOIN Account a
        ON c.CustomerID = a.CustomerID
        WHERE c.CustomerID = ?
        """

        self.cur.execute(sql, (custid,))

        return self.cur.fetchall()

    def searchcustomer(self, name):

        sql = """
        SELECT *
        FROM Customer
        WHERE Name LIKE ?
        """

        self.cur.execute(
            sql,
            ("%" + name + "%",)
        )

        return self.cur.fetchall()

    # ---------------------------
    # Account
    # ---------------------------
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
            """
            UPDATE Account
            SET Balance = Balance + ?
            WHERE AccountNumber = ?
            """,
            (amt, accno)
        )

        self.conn.commit()

    # ---------------------------
    # Withdraw
    # ---------------------------

    def withdraw(self, accno, amt):

        self.cur.execute(
            """
            UPDATE Account
            SET Balance = Balance - ?
            WHERE AccountNumber = ?
            """,
            (amt, accno)
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
            sql = """
            SELECT
                TransactionID,
                AccountNumber,
                TransactionType,
                Amount,
                TransactionDate
            FROM [Transaction]
            WHERE AccountNumber = ?
            ORDER BY TransactionDate DESC
            """

            self.cur.execute(sql, (accno,))

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