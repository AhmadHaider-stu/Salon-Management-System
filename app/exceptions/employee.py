class UsedPhoneNumber(Exception):
    def __init__(self):
        super().__init__('Already in employees')

class NotFoundEmployee(Exception):
    def __init__(self):
        super().__init__('Employee not found')

class EmployeeBusy(Exception):
    def __init__(self):
        super().__init__('Employee busy')


class EmployeeNotAssigned(Exception):
    def __init__(self):
        super().__init__('Employee cannot do this service')


class InactiveEmployee(Exception):
    def __init__(self):
        super().__init__('Employee is not active')

class EmployeeHasHistory(Exception):
    def __init__(self):
        super().__init__('Service has active appointments')

class InvalidPhoneNumber(Exception):
    def __init__(self):
        super().__init__('Invalid phone number')