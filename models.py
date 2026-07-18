"""
=========================================
File : models.py
Purpose : Bank Models
=========================================
"""


# ==========================================
# Person (Parent Class)
# ==========================================

class Person:

    # Create person object
    def __init__(self, name, phone, user, passw):

        self.name = name
        self.phone = phone
        self.user = user
        self.passw = passw


# ==========================================
# Manager
# ==========================================

class Manager(Person):

    # Create manager object
    def __init__(self, mgrId, name, phone, user, passw):

        super().__init__(name, phone, user, passw)

        self.mgrId = mgrId


# ==========================================
# Employee
# ==========================================

class Employee(Person):

    # Create employee object
    def __init__(self, empId, mgrId, name, phone, user, passw):

        super().__init__(name, phone, user, passw)

        self.empId = empId
        self.mgrId = mgrId


# ==========================================
# Customer
# ==========================================

class Customer(Person):

    # Create customer object
    def __init__(self, custId, empId, name, phone, address, user, passw):

        super().__init__(name, phone, user, passw)

        self.custId = custId
        self.empId = empId
        self.address = address


# ==========================================
# Account
# ==========================================

class Account:

    # Create account object
    def __init__(self, accId, custId, accNo, accType, bal):

        self.accId = accId
        self.custId = custId
        self.accNo = accNo
        self.accType = accType

        # Private variable (Encapsulation)
        self.__bal = bal

    # Add money
    def deposit(self, amt):

        self.__bal += amt

    # Remove money
    def withdraw(self, amt):

        self.__bal -= amt

    # Get balance
    def getBal(self):

        return self.__bal


# ==========================================
# Savings Account
# ==========================================

class SavingsAccount(Account):

    def __init__(self, accId, custId, accNo, bal):

        super().__init__(accId, custId, accNo, "Savings", bal)

    # Polymorphism
    def interest(self):

        return self.getBal() * 0.04


# ==========================================
# Current Account
# ==========================================

class CurrentAccount(Account):

    def __init__(self, accId, custId, accNo, bal):

        super().__init__(accId, custId, accNo, "Current", bal)

    # Polymorphism
    def interest(self):

        return 0


# ==========================================
# Transaction
# ==========================================

class Transaction:

    # Create transaction object
    def __init__(self, transId, accNo, transType, amt):

        self.transId = transId
        self.accNo = accNo
        self.transType = transType
        self.amt = amt