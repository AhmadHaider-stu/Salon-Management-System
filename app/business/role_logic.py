from app.CRUD.user import *
from app.exceptions.user import *
from app.exceptions.client import ClientHasHistory
from app.business.employee_logic import *
from app.CRUD.employee_service import del_service_by_employee 
from app.CRUD.appointment_service import *
from app.CRUD.client import del_client
from app.business.client_logic import register_client
from app.services.phone_validation import is_valid_phone, format_phone
from app.models.appointment import *


# HELPER 

def get_user_or_raise(session, userID):
    user = get_user(session, userID)

    if user[0] == "FAIL":
        raise NotFound()

    return user

def check_admin(user):
    if (user.role != Role.ADMIN):
        raise IsNotAdmin()
    

# ADMIN FUNCTIONS


def register_employee(session , f_name , l_name , email , phone, photo = None , socialMedia = None , active = True ):
    try:
        f_name = f_name.upper()
        l_name = l_name.upper()
        if not is_valid_phone(phone, "AE"):
            raise InvalidPhoneNumber()
        phone = format_phone(phone, "AE")
        employee = get_employee_by_email(session=session , email=email)
        if employee[1] != None:
            raise IsEmployee()

        employee = add_employee(session = session
                            , f_name = f_name 
                            , l_name = l_name 
                            , email = email 
                            , photo = photo 
                            , socialMedia = socialMedia 
                            , active = active
                            , phone = phone)
        return employee
    except :
        raise    

def make_employee(session , current_user, userID):
    try:
        check_admin(current_user)
        user=get_user_or_raise(session=session,userID=userID)
        if (user[1].role != Role.CLIENT):
            raise IsEmployee()
        user = user[1]
        
        active_appointments = session.query(Appointment).filter(
        Appointment.client_id == user.client_id,
        Appointment.status.in_([AppointmentStatus.PENDING, AppointmentStatus.CONFIRMED])
        ).first()
        if active_appointments is not None:
            raise ClientHasHistory()
        if user.client_id is not None:
            del_client(session=session, clientID=user.client_id)
            user.client_id = None
        
        employee = register_employee(session=session
                                     ,f_name = user.f_name 
                                     ,l_name = user.l_name 
                                     ,email = user.email
                                     ,phone = user.phone)
        
        user.employee_id = employee.id
        user.role = Role.EMPLOYEE
        session.commit()
        return employee
    except:
        session.rollback()
        raise

def delete_employee(session, current_user, userID):
    try:
        check_admin(current_user)
        user = get_user_or_raise(session=session, userID=userID)

        if user[1].employee_id is None:
            raise IsClient()
        user = user[1]
        employee = get_employee(session=session, employeeID=user.employee_id)[1]

        active_appointments = session.query(AppointmentService).filter(
            AppointmentService.employee_id == employee.id,
            AppointmentService.status.in_([AppointmentStatus.PENDING, AppointmentStatus.CONFIRMED])
        ).first()
        if active_appointments is not None:
            raise EmployeeHasHistory()  

        del_service_by_employee(session=session, employeeID=employee.id)
        del_appointment_by_employee(session=session, employeeID=employee.id)  # only removes PENDING rows
        email = employee.email
        del_employee(session=session, employee=employee)
        user.employee_id = None
        client = register_client(session=session, f_name=user.f_name, l_name=user.l_name, email=email)
        user.role = Role.CLIENT
        user.client_id = client.id
        session.commit()
        return user 
    except:
        session.rollback()
        raise


def make_admin(session, current_user, userID):
    try:
        check_admin(current_user)
        user = get_user_or_raise(session=session, userID=userID)
        if user[1].employee_id is None:
            raise IsClient()
        user = user[1]

        if user.client_id is None:
            client = register_client(session=session, f_name=user.f_name, l_name=user.l_name, email=user.email , phone = user.phone)
            user.client_id = client.id

        user.role = Role.ADMIN
        session.commit()
        return user
    except:
        session.rollback()
        raise

def delete_admin(session ,current_user, userID):
    try:
        check_admin(current_user)
        user = get_user_or_raise(session=session, userID=userID)
        if user[1].employee_id is None:
            raise IsClient()
        user = user[1]
        employee = get_employee(session=session, employeeID=user.employee_id)[1]
        del_employee(session=session, employee=employee)
        
        user.employee_id = None
        user.role = Role.CLIENT
        session.commit()
        return user
    except:
        session.rollback()
        raise

def make_receptionist(session ,current_user, userID):
    try:
        check_admin(current_user)

        user = get_user_or_raise(session=session,userID=userID)
        if (user[1].employee_id == None):
            raise IsClient()
        user = user[1]
        if user.client_id is None:
            client = register_client(session=session, f_name=user.f_name, l_name=user.l_name, email=user.email , phone = user.phone)
            user.client_id = client.id
        user.role = Role.RECEPTION
        session.commit()
        return user
    except:
        session.rollback()
        raise

def delete_receptionist(session, current_user, userID):
    try:
        check_admin(current_user)
        user = get_user_or_raise(session=session, userID=userID)
        if user[1].employee_id is None:
            raise IsClient()
        user = user[1]
        employee = get_employee(session=session, employeeID=user.employee_id)[1]
        del_employee(session=session, employee=employee)

        user.employee_id = None
        user.role = Role.CLIENT
        session.commit()
        return user
    except:
        session.rollback()
        raise