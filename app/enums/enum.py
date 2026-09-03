import enum

class AppointmentStatus(enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    NO_SHOW = 'no_show'

class Role(enum.Enum):
    CLIENT = 'client'
    ADMIN = 'admin'
    EMPLOYEE = 'employee'
    RECEPTION = 'receptionist'

class ServiceCategory(enum.Enum):
    HAIR = 'hair styling'
    NAIL = 'nails'
    MAKEUP = 'makeup'
    WAXING = 'Threading and waxing'
    FACIAL = 'facial treatment'

class Provider(enum.Enum):
    GOOGLE = 'google'
    FACEBOOK = 'facebook'

class DayOfWeek(enum.Enum):
    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"
    SUNDAY = "sunday"