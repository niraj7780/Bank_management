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
    # Password Hash
    # ---------------------------

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

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
        VALUES
        (
            ?, ?, ?, ?
        )
        """

        self.cur.execute(
            sql,
            (name, phone, user, pwd)
        )

        self.conn.commit()

        self.cur.execute("SELECT SCOPE_IDENTITY()")
        return int(self.cur.fetchone()[0])

    # NOTE:
    # Keep the rest of your methods exactly the same as in your current file.
    # Only make these additional changes:
    #
    # 1. In addcustomer():
    #    password = self.hash_password(password)
    #    After commit:
    #       self.cur.execute("SELECT SCOPE_IDENTITY()")
    #       return int(self.cur.fetchone()[0])
    #
    # 2. Remove the duplicate hash_password() from the bottom.
    #
    # 3. In transfer():
    #    except pyodbc.Error as e:
    #        self.conn.rollback()
    #        print("Database Error:", e)
