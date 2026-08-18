class UserAlreadyExists(Exception):
    def __init__(self, ):
        super().__init__('User already signed in')

class NotFound(Exception):
    def __init__(self, ):
        super().__init__('User not found')

class IsClient(Exception):
    def __init__(self, ):
        super().__init__('User is client')

class IsNotAdmin (Exception):
    def __init__(self):
        super().__init__('User is not admin')

class IsEmployee (Exception):
    def __init__(self):
        super().__init__('User is employee')

class IsBlocked(Exception):
    def __init__(self):
        super().__init__('User is blocked')

class InvalidPhoneNumber(Exception):
    def __init__(self):
        super().__init__('Invalid phone number')

class UsedPhoneNumber(Exception):
    def __init__(self):
        super().__init__('Used phone number')