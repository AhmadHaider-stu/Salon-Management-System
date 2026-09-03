from datetime import datetime, time
from calendar import monthrange
from app.CRUD.appointment_service import *
from app.CRUD.appointment import *
from app.enums.enum import AppointmentStatus, Role
from app.CRUD.client import *
from zoneinfo import ZoneInfo
now = datetime.now(ZoneInfo("Asia/Amman"))

def get_employee_calendar_day(session, employeeID, date, viewer):
    day_start = datetime.combine(date, time.min)
    day_end = datetime.combine(date, time.max)
    include_cancelled = viewer.role in (Role.ADMIN, Role.RECEPTION)

    query = session.query(AppointmentService, Client.f_name, Client.l_name).join(
        Appointment, AppointmentService.appointment_id == Appointment.id
    ).join(
        Client, Appointment.client_id == Client.id
    ).filter(
        AppointmentService.employee_id == employeeID,
        AppointmentService.start_time >= day_start,
        AppointmentService.start_time <= day_end,
    )
    if not include_cancelled:
        query = query.filter(AppointmentService.status != AppointmentStatus.CANCELLED)

    results = query.order_by(AppointmentService.start_time).all()

    output = []
    for service, f_name, l_name in results:
        output.append({
            "id": service.id,
            "appointment_id": service.appointment_id,
            "service_id": service.service_id,
            "employee_id": service.employee_id,
            "start_time": service.start_time,
            "end_time": service.end_time,
            "price": service.price,
            "status": service.status,
            "reminder": service.reminder,
            "client_name": f"{f_name} {l_name}",
        })
    return output


def get_employee_calendar_month(session, employeeID, year, month, viewer):
    include_cancelled = viewer.role in (Role.ADMIN, Role.RECEPTION)
    days_in_month = monthrange(year, month)[1]

    month_start = datetime(year, month, 1, 0, 0, 0)
    month_end = datetime(year, month, days_in_month, 23, 59, 59)

    query = session.query(AppointmentService, Client.f_name, Client.l_name).join(
        Appointment, AppointmentService.appointment_id == Appointment.id
    ).join(
        Client, Appointment.client_id == Client.id
    ).filter(
        AppointmentService.employee_id == employeeID,
        AppointmentService.start_time >= month_start,
        AppointmentService.start_time <= month_end,
    )
    if not include_cancelled:
        query = query.filter(AppointmentService.status != AppointmentStatus.CANCELLED)

    results = query.order_by(AppointmentService.start_time).all()

    buckets = {str(day): [] for day in range(1, days_in_month + 1)}
    for service, f_name, l_name in results:
        entry = {
            "id": service.id,
            "appointment_id": service.appointment_id,
            "service_id": service.service_id,
            "employee_id": service.employee_id,
            "start_time": service.start_time,
            "end_time": service.end_time,
            "price": service.price,
            "status": service.status,
            "reminder": service.reminder,
            "client_name": f"{f_name} {l_name}",
        }
        buckets[str(service.start_time.day)].append(entry)
    return buckets


def get_salon_calendar_day(session, date):
    day_start = datetime.combine(date, time.min)
    day_end = datetime.combine(date, time.max)
    return session.query(Appointment).filter(
        Appointment.start_time >= day_start,
        Appointment.start_time <= day_end,
    ).order_by(Appointment.start_time).all()


def get_salon_calendar_month(session, year, month):
    days_in_month = monthrange(year, month)[1]
    month_start = datetime(year, month, 1, 0, 0, 0)
    month_end = datetime(year, month, days_in_month, 23, 59, 59)

    results = session.query(Appointment).filter(
        Appointment.start_time >= month_start,
        Appointment.start_time <= month_end,
    ).order_by(Appointment.start_time).all()

    buckets = {str(day): [] for day in range(1, days_in_month + 1)}
    for row in results:
        buckets[str(row.start_time.day)].append(row)
    return buckets