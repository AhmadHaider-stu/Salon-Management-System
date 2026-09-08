from app.models.appointment_service import *
from app.enums.enum import *



def add_appointment_service (session , appointmentID , serviceID , employeeID , price , start_time , end_time , status = AppointmentStatus.PENDING , reminder = 0):
    new_appointment_service = AppointmentService(appointment_id = appointmentID , service_id = serviceID , employee_id = employeeID ,price = price , start_time = start_time , end_time = end_time , reminder = reminder ,status = status)
    session.add(new_appointment_service)
    session.flush()
    return new_appointment_service

def del_appointment_service (session ,appointment_serviceID):
    appointment = session.query(AppointmentService).filter(AppointmentService.id == appointment_serviceID).one_or_none()
    session.delete(appointment)

def del_appointment_by_employee(session , employeeID):
    appointments = session.query(AppointmentService).filter(AppointmentService.employee_id == employeeID).all()
    for row in appointments:
        session.delete(row)
    session.flush()

def del_appointment_by_service(session , serviceID):
    appointments = session.query(AppointmentService).filter(AppointmentService.service_id == serviceID ).all()
    for row in appointments:
        session.delete(row)
    session.flush()

def del_appointment_by_appointment(session , appointmentID):
    appointments = session.query(AppointmentService).filter(AppointmentService.appointment_id == appointmentID , AppointmentService.status == AppointmentStatus.PENDING).all()
    for row in appointments:
        session.delete(row)
    session.flush()


def get_appointment_service(session , appointment_serviceID):
    appointment = session.query(AppointmentService).filter(AppointmentService.id == appointment_serviceID).one_or_none()
    if (appointment == None):
        return 'FAIL',None
    return 'OK',appointment

def get_appointment_service_by_appointment(session , appointmentID):
    appointments = session.query(AppointmentService).filter(AppointmentService.appointment_id == appointmentID).all()
    if (len(appointments) == 0):
        return 'FAIL',None
    return 'OK',appointments


def update_appointment_service_reminder(session, AppointmentServiceID, newReminder):
    status, appointment = get_appointment_service(session=session, AppointmentServiceID=AppointmentServiceID)
    if status == 'FAIL':
        return 'FAIL'
    appointment.reminder = newReminder
    session.flush()
    return 'OK'


def get_employee_appointments(session,employeeID):
    appointments = session.query(AppointmentService).filter(AppointmentService.employee_id == employeeID)
    return appointments
