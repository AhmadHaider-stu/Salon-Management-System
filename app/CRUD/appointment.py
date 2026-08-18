from app.models.appointment import *
from sqlalchemy import Enum 
from app.enums.enum import *

def add_appointment(session, clientID, phone, start_time, end_time, note = None,total=0, status=AppointmentStatus.PENDING):
    new_appointment = Appointment(
        client_id=clientID,
        phone=phone,
        start_time=start_time,
        end_time=end_time,
        total_price=total,
        status=status,
        note = note
    )
    session.add(new_appointment)
    session.flush()
    return new_appointment

# Appointment cancellation from the client (all the appointment canceled not a service of it) -->> not allowed for now
def del_appointment(session, appointmentID):
    appointment = get_appointment(session=session,appointmentID=appointmentID)
    session.delete(appointment[1])


def del_appointments_client(session , clientID):
    all = session.query(Appointment).filter(Appointment.client_id == clientID).all()
    for row in all:
        session.delete(row)
    return 'OK'

def get_appointment(session , appointmentID):
    appointment = session.query(Appointment).filter(Appointment.id == appointmentID).one_or_none()
    if appointment == None:
        return 'FAIL',None
    return 'OK',appointment

def update_appointment_status(session, appointmentID, newStatus):
    status, appointment = get_appointment(session=session, appointmentID=appointmentID)
    if status == 'FAIL':
        return 'FAIL'
    appointment.status = newStatus
    session.flush()
    return 'OK'
def get_client_appointment(session , clientID):
    appointments = session.query(Appointment).filter(Appointment.client_id == clientID).all()
    return appointments

