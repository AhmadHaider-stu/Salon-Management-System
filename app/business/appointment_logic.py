from sqlalchemy import func
from app.CRUD.appointment_service import *
from app.CRUD.appointment import *
from app.business.service_logic import get_or_raise as service_get_or_raise 
from app.CRUD.client import get_client
from app.CRUD.employee import get_employee
from app.CRUD.employee_service import EmployeeService
from app.CRUD.user import get_user_by_email
from datetime import timedelta,datetime , time
from app.exceptions.client import * 
from app.exceptions.employee import * 
from app.exceptions.user import * 
from app.exceptions.appointments import *
from app.CRUD.employee_schedule import get_schedule_for_day
from app.business.reminders import send_confirmation_emails, send_completion_email




#### CHANGE EMPLOYEE STATUS TOTAL HOURS
BREAK_MINUTES = 10

#HELPER 

def get_or_raise (session , appointmentID):
        status ,appointment= get_appointment(session=session,appointmentID=appointmentID)
        if (status == 'FAIL'):
            raise NotFoundAppointment()
        return appointment

def get_or_raise_appointment_service(session , appointment_serviceID):
    status ,appointment= get_appointment_service(session=session,appointment_serviceID=appointment_serviceID)
    if (status == 'FAIL'):
        raise NotFoundAppointment()
    return appointment

def recalculate_total(session , appointmentID):
    total = session.query(func.sum(AppointmentService.price)).filter(AppointmentService.appointment_id == appointmentID).scalar()
    return total or 0

def recalculate_schedule(session ,appointment):
    newStart = appointment.start_time
    end = newStart

    appointment_services = get_appointment_service_by_appointment(session=session,appointmentID=appointment.id)[1]
    for appointment_service in appointment_services :
        appointment_service.start_time = newStart
        service = service_get_or_raise(session=session,serviceID=appointment_service.service_id)
        appointment_service.end_time = (
        newStart + timedelta(minutes=service.time_duration)
        )
        end = appointment_service.end_time
        newStart = appointment_service.end_time + timedelta(minutes=BREAK_MINUTES)
    return end

def compute_schedule(session, employee_servicesIDs, start_time):
    """Compute each service's start/end time and price in memory — no DB writes."""
    newStart = start_time
    schedule = []
    for item in employee_servicesIDs:
        service = service_get_or_raise(session=session, serviceID=item.service_id)
        end = newStart + timedelta(minutes=service.time_duration)
        schedule.append({
            "employee_id": item.employee_id,
            "service_id": item.service_id,
            "start_time": newStart,
            "end_time": end,
            "price": service.price,
        })
        newStart = end + timedelta(minutes=BREAK_MINUTES)
    return schedule

def is_employee_free(session , employeeID , start_time,end_time,exclude_appointment_service_id=None):
    day_of_week = DayOfWeek(start_time.strftime('%A').lower())  # confirm this matches your enum values exactly
    status, schedule = get_schedule_for_day(session=session, employee_id=employeeID, day_of_week=day_of_week)
    if status == 'FAIL':
        return False 

    if start_time.time() < schedule.start_time or end_time.time() > schedule.end_time:
        return False  
    start_day = datetime.combine(start_time.date() , time.min)
    end_day = datetime.combine(start_time.date(),time.max)
    query = session.query(AppointmentService).filter(
        AppointmentService.employee_id == employeeID,
        AppointmentService.status.in_([AppointmentStatus.PENDING,AppointmentStatus.CONFIRMED]),
        AppointmentService.start_time >= start_day,
        AppointmentService.end_time <= end_day
    )
    buffered_start = start_time - timedelta(minutes=BREAK_MINUTES)
    buffered_end = end_time + timedelta(minutes=BREAK_MINUTES)
    if exclude_appointment_service_id:
        query = query.filter(AppointmentService.appointment_id != exclude_appointment_service_id)
    for existing in query.all():
        print(existing.start_time , buffered_end , existing.end_time , buffered_start , sep='---')
        if existing.start_time < buffered_end and existing.end_time > buffered_start:
            return False
    
    return True

def is_client_free(session, client_id, exclude_appointment_id=None):
    
    query = session.query(Appointment).filter(
        Appointment.client_id == client_id,
        Appointment.status.in_([AppointmentStatus.PENDING, AppointmentStatus.CONFIRMED]),
    )
    if exclude_appointment_id:
        query = query.filter(Appointment.id != exclude_appointment_id)
    existing = query.all()
    if len(existing) > 0:
        return False
    return True


def check_employee_service (session , employeeID , serviceID):
        isExist = session.query(EmployeeService).filter(
            EmployeeService.employee_id == employeeID,
            EmployeeService.service_id == serviceID
        ).one_or_none()
        employee = get_employee(session=session,employeeID=employeeID)[1]
        if (employee == None):
            raise NotFoundEmployee()
        if (employee.active == False):
            raise InactiveEmployee()
        if (isExist == None):
            raise EmployeeNotAssigned()
        return True
    

def check_client(session, clientID, exclude):
    status, client = get_client(session=session, clientID=clientID)
    if client is None:
        raise NotFoundClient()
    user_status, user = get_user_by_email(session=session, email=client.email)
    if user_status=='OK' and user.block == 1:
        raise IsBlocked()
    isFree = is_client_free(session=session, client_id=clientID, exclude_appointment_id=exclude)
    if isFree == False:
        raise DoubleBook()

def validate_booking(session, clientID, schedule, exclude):
    check_client(session=session, clientID=clientID, exclude=exclude)
    for entry in schedule:
        if not check_employee_service(session=session, employeeID=entry["employee_id"], serviceID=entry["service_id"]):
            raise EmployeeNotAssigned()
        if not is_employee_free(session=session, employeeID=entry["employee_id"],
                                 start_time=entry["start_time"], end_time=entry["end_time"],
                                 exclude_appointment_service_id=exclude):
            raise EmployeeBusy()
    return True

def delete_if_empty(session , appointmentID):
    if (get_appointment_service_by_appointment(session=session,appointmentID=appointmentID)[0]=='FAIL'):
        del_appointment(session=session,appointmentID=appointmentID)
        return True
    return False
    

# FUNCTIONS : BOOK , RESCHEDULE , CHANGE STATUS , SELECT EMPLOYEE MAUNALLY 

def book_appointment(session, clientID,  employee_servicesIDs, start_time,note= None):
    try:
        status, client = get_client(session=session, clientID=clientID)
        if status == 'FAIL':
            raise NotFoundClient()
        schedule = compute_schedule(session=session, employee_servicesIDs=employee_servicesIDs, start_time=start_time)
        validate_booking(session=session, clientID=clientID, schedule=schedule, exclude=None)

        appointment = add_appointment(
            session=session, clientID=clientID, phone=client.phone,
            start_time=schedule[0]["start_time"], end_time=schedule[-1]["end_time"],note = note
        )

        total = 0
        for entry in schedule:
            add_appointment_service(
                session=session, appointmentID=appointment.id,
                serviceID=entry["service_id"], employeeID=entry["employee_id"],
                price=entry["price"], start_time=entry["start_time"], end_time=entry["end_time"]
            )
            total += entry["price"]

        appointment.total_price = total
        session.commit()
        return appointment
    except:
        session.rollback()
        raise


def change_appointment_status(session , appointmentID, status):
    appointment = get_or_raise(session=session,appointmentID=appointmentID)
    appointment.status = status
    change_appointment_service_status(session=session,appointmentID=appointmentID , status=status)
    session.commit()

# add to employee hours and services total_order 
def change_appointment_service_status(session , appointmentID , status):
    appointments = get_appointment_service_by_appointment(session=session, appointmentID=appointmentID)[1]
    for appointment in appointments:
        appointment.status = status 
    
def delete_appointment_service(session , appointment_serviceID):
    appointment_service = get_or_raise_appointment_service(session=session,appointment_serviceID=appointment_serviceID)
    appointment_id = appointment_service.appointment_id 
    del_appointment_service(session=session,appointment_serviceID=appointment_serviceID)
    empty = delete_if_empty(session=session,appointmentID=appointment_id)
    if (not empty):
        appointment = get_or_raise(session=session,appointmentID=appointment_id)
        appointment.total_price = recalculate_total(session=session,appointmentID=appointment_id)
        appointment.end_time = recalculate_schedule(session=session,appointment=appointment)
    session.commit()
    return empty
    
def delete_appointment(session , appointmentID):
    appointment = get_or_raise(session=session,appointmentID=appointmentID)
    appointments = get_appointment_service_by_appointment(session=session, appointmentID=appointmentID)[1]
    for appointment_service in appointments:
        del_appointment_service(session=session,appointment_serviceID=appointment_service.id)
    session.delete(appointment)
    session.commit()
    return 'OK'


def change_appointment_status(session, appointmentID, status):
    appointment = get_appointment(session=session, appointmentID=appointmentID)[1]
    appointment.status = status
    change_appointment_service_status(session=session, appointmentID=appointmentID, status=status)
    session.commit()

    if status == AppointmentStatus.CONFIRMED and not appointment.confirmation_sent:
        send_confirmation_emails(session=session, appointmentID=appointmentID)
        appointment.confirmation_sent = True
        session.commit()
    elif status == AppointmentStatus.COMPLETED:
        send_completion_email(session=session, appointmentID=appointmentID)