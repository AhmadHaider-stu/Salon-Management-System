from datetime import datetime, timedelta, date as date_type, time
from app.models.client import Client
from app.models.service import Service
from app.models.employee import Employee
from app.models.appointment import Appointment
from app.models.appointment_service import AppointmentService
from app.enums.enum import AppointmentStatus


def get_dashboard_summary(session):
    total_customers = session.query(Client).count()
    total_appointments = session.query(Appointment).count()
    total_accepted = session.query(Appointment).filter(
        Appointment.status.in_([AppointmentStatus.CONFIRMED, AppointmentStatus.COMPLETED])
    ).count()
    total_rejected = session.query(Appointment).filter(
        Appointment.status == AppointmentStatus.CANCELLED
    ).count()
    total_services = session.query(Service).count()

    yesterday = date_type.today() - timedelta(days=1)
    yesterday_start = datetime.combine(yesterday, time.min)
    yesterday_end = datetime.combine(yesterday, time.max)
    yesterday_appointments = session.query(Appointment).filter(
        Appointment.start_time >= yesterday_start,
        Appointment.start_time <= yesterday_end,
    ).count()

    now = datetime.now()
    upcoming_appointments = session.query(Appointment).filter(
        Appointment.start_time >= now,
        Appointment.status.in_([AppointmentStatus.PENDING, AppointmentStatus.CONFIRMED]),
    ).count()

    return {
        "total_customers": total_customers,
        "total_appointments": total_appointments,
        "total_accepted": total_accepted,
        "total_rejected": total_rejected,
        "total_services": total_services,
        "yesterday_appointments": yesterday_appointments,
        "upcoming_appointments": upcoming_appointments,
    }


def get_stylists_overview(session):
    employees = session.query(Employee).filter(Employee.active == True).all()
    today = date_type.today()
    today_start = datetime.combine(today, time.min)
    today_end = datetime.combine(today, time.max)

    result = []
    for emp in employees:
        count_today = session.query(AppointmentService).filter(
            AppointmentService.employee_id == emp.id,
            AppointmentService.start_time >= today_start,
            AppointmentService.start_time <= today_end,
            AppointmentService.status != AppointmentStatus.CANCELLED,
        ).count()
        result.append({
            "id": emp.id,
            "name": f"{emp.f_name} {emp.l_name}",
            "photo": emp.photo,
            "appointments_today": count_today,
        })
    return result


def get_appointments_by_hour(session, date):
    day_start = datetime.combine(date, time.min)
    day_end = datetime.combine(date, time.max)

    appointments = session.query(Appointment).filter(
        Appointment.start_time >= day_start,
        Appointment.start_time <= day_end,
        Appointment.status.in_([AppointmentStatus.COMPLETED ,AppointmentStatus.CONFIRMED, AppointmentStatus.PENDING])
    ).all()

    buckets = {str(h): 0 for h in range(24)}
    for appt in appointments:
        buckets[str(appt.start_time.hour)] += 1
    return buckets