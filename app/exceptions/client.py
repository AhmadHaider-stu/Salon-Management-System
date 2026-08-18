class NotFoundClient(Exception):
    def __init__(self):
        super().__init__('Client not found')

class DoubleBook(Exception):
    def __init__(self):
        super().__init__('Cannot book more than one appointment a day')

class InvalidPhoneNumber(Exception):
    def __init__(self):
        super().__init__('Invalid phone number')

class ClientHasHistory(Exception):
    def __init__(self):
        super().__init__('Client has appointments')

class ClientHasAccount(Exception):
    def __init__(self):
        super().__init__('Client has account already')
