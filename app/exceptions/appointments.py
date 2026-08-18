
class DuplicatePendingAppointment (Exception):
    def __init__(self) :
        super().__init__('Client already has a pending appointment')

class NotActiveEmployee (Exception):
    def __init__(self):
        super().__init__('Employee not active')

class NotActiveService (Exception):
    def __init__(self):
        super().__init__('Service not active')

class NotAvailableEmployee (Exception):
    def __init__(self):
        super().__init__('Employee not available')
class NotFoundAppointment(Exception):
    def __init__(self):
        super().__init__('Appointment not found')

class CannotModifyAppointment(Exception):
    def __init__(self):
        super().__init__('Cannot change this appointment')

