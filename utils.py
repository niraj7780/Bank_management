"""
=========================================
File : utils.py
Purpose : Helper Functions
=========================================
"""

import random


# Check phone number
def validphone(phone):

    if len(phone) != 10:
        return False

    if not phone.isdigit():
        return False

    return True


# Check username
def validuser(user):

    if len(user) < 4:
        return False

    return True


# Check password
def validpwd(pwd):

    if len(pwd) < 4:
        return False

    return True


# Check amount
def validamt(amt):

    try:

        amt = float(amt)

        if amt <= 0:
            return False

        return True

    except:

        return False


# Generate account number
def genaccno():

    no = random.randint(100001,999999)

    return "ACC" + str(no)