"""
=========================================
File : exceptions.py
Purpose : Custom Exceptions
=========================================
"""


# Base exception
class BankError(Exception):
    pass


# Login error
class LoginError(BankError):
    pass


# Account not found
class AccountError(BankError):
    pass


# Low balance
class BalanceError(BankError):
    pass


# Duplicate username
class UserError(BankError):
    pass


# Invalid amount
class AmountError(BankError):
    pass


# Database error
class DatabaseError(BankError):
    pass