

class InvalidPhoneError(Exception):

    def __init__(self, message="Phone number must contain exactly 10 digits."):
        super().__init__(message)


class InvalidUsernameError(Exception):

    def __init__(self, message="Username must be at least 4 characters long."):
        super().__init__(message)


class InvalidPasswordError(Exception):

    def __init__(self, message="Password must contain at least 8 characters."):
        super().__init__(message)


class CustomerNotFoundError(Exception):

    def __init__(self, message="Customer not found."):
        super().__init__(message)



class AccountNotFoundError(Exception):

    def __init__(self, message="Account not found."):
        super().__init__(message)



class InsufficientBalanceError(Exception):

    def __init__(self, message="Insufficient account balance."):
        super().__init__(message)



class InvalidAmountError(Exception):

    def __init__(self, message="Amount must be greater than zero."):
        super().__init__(message)


class UsernameExistsError(Exception):

    def __init__(self, message="Username already exists."):
        super().__init__(message)



class MinimumBalanceError(Exception):

    def __init__(self, message="Minimum opening balance is 1000."):
        super().__init__(message)