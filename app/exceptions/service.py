class DuplicateService(Exception):
    def __init__(self):
        super().__init__('Service exists')


class NotFoundService(Exception):
    def __init__(self):
        super().__init__('Service not found')

class ServiceHasHistory(Exception):
    def __init__(self):
        super().__init__('Service has active appointments')
