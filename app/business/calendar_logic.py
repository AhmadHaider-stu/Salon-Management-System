from datetime import datetime, time
from calendar import monthrange
from app.CRUD.appointment_service import *
from app.CRUD.appointment import *
from app.enums.enum import AppointmentStatus, Role


def get_employee_calendar_day(session, employeeID, date, viewer):
    day_start = datetime.combine(date, time.min)
    day_end = datetime.combine(date, time.max)
    include_cancelled = viewer.role in (Role.ADMIN, Role.RECEPTION)

    query = session.query(AppointmentService).filter(
        AppointmentService.employee_id == employeeID,
        AppointmentService.start_time >= day_start,
        AppointmentService.start_time <= day_end,
    )
    if not include_cancelled:
        query = query.filter(AppointmentService.status != AppointmentStatus.CANCELLED)

    return query.order_by(AppointmentService.start_time).all()


def get_employee_calendar_month(session, employeeID, year, month, viewer):
    include_cancelled = viewer.role in (Role.ADMIN, Role.RECEPTION)
    days_in_month = monthrange(year, month)[1]

    month_start = datetime(year, month, 1, 0, 0, 0)
    month_end = datetime(year, month, days_in_month, 23, 59, 59)

    query = session.query(AppointmentService).filter(
        AppointmentService.employee_id == employeeID,
        AppointmentService.start_time >= month_start,
        AppointmentService.start_time <= month_end,
    )
    if not include_cancelled:
        query = query.filter(AppointmentService.status != AppointmentStatus.CANCELLED)

    results = query.order_by(AppointmentService.start_time).all()

    buckets = {str(day): [] for day in range(1, days_in_month + 1)}
    for row in results:
        buckets[str(row.start_time.day)].append(row)
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