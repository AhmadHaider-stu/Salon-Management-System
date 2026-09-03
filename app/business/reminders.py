from datetime import datetime, timedelta

from app.services.email_client import send_email
from app.CRUD.appointment import get_appointment
from app.CRUD.appointment_service import get_appointment_service_by_appointment
from app.CRUD.client import get_client
from app.CRUD.employee import get_employee
from app.models.appointment_service import AppointmentService
from app.enums.enum import AppointmentStatus
from zoneinfo import ZoneInfo
now = datetime.now(ZoneInfo("Asia/Amman"))


def send_confirmation_emails(session, appointmentID):
    status, appointment = get_appointment(session=session, appointmentID=appointmentID)
    if status == 'FAIL':
        return

    client_status, client = get_client(session=session, clientID=appointment.client_id)
    if client_status == 'OK' and client.email:
        send_email(
            client.email,
            "Appointment Confirmed",
            f"Hi {client.f_name}, your appointment on {appointment.start_time} is confirmed. Thank you for choosing us <3."
        )

    services_status, services = get_appointment_service_by_appointment(session=session, appointmentID=appointmentID)
    if services_status == 'OK':
        for entry in services:
            emp_status, employee = get_employee(session=session, employeeID=entry.employee_id)
            if emp_status == 'OK' and employee.email :
                send_email(
                    employee.email,
                    "New Appointment Confirmed",
                    f"Hi {employee.f_name}, you have a confirmed booking at {entry.start_time}."
                )
                # entry.reminder = True


def send_completion_email(session, appointmentID):
    status, appointment = get_appointment(session=session, appointmentID=appointmentID)
    if status == 'FAIL':
        return
    services_status, services = get_appointment_service_by_appointment(session=session, appointmentID=appointmentID)
    if services_status == 'OK':
        for entry in services:
                if entry.reminder == 1:
                    return 
                else:
                    entry.reminder = True
    client_status, client = get_client(session=session, clientID=appointment.client_id)
    if client_status == 'OK' and client.email:
        send_email(
            client.email,
            "Thank You For Visiting",
            f"Hi {client.f_name}, thank you for visiting us today!"
        )

def send_pending_reminders(session):
    now = datetime.now()
    window_end = now + timedelta(minutes=5)

    services = session.query(AppointmentService).filter(
        AppointmentService.status == AppointmentStatus.CONFIRMED,
        AppointmentService.reminder == False,
        AppointmentService.start_time >= now,
        AppointmentService.start_time <= window_end,
    ).all()

    for entry in services:
        status, employee = get_employee(session=session, employeeID=entry.employee_id)
        if status == 'OK' and employee.email:
            send_email(employee.email, "Upcoming Appointment Reminder",
                        f"Hi {employee.f_name}, you have an appointment at {entry.start_time}.")
        entry.reminder = True

    session.commit()