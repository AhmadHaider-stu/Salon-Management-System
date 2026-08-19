from app.CRUD.service import *
from app.exceptions.service import *
from app.exceptions.employee import *
from app.CRUD.employee_service import *
from app.CRUD.appointment_service import *

#HELPER FUNCTIONS 
def get_or_raise(session , serviceID):
    service = get_service(serviceID=serviceID , session=session)
    if ( service[0]== 'FAIL'):
        raise NotFoundService()
    return service[1]


# SERVICES FUNCTIONS 
def create_service(session , category , description , price , time_duration):
    try :
        description = description.upper()
        if (get_service_by(session=session , category=category , description=description)[0] == 'OK'):
            raise DuplicateService()
        service = add_service(session=session,category=category,description=description,price=price,time_duration=time_duration)[1]
        session.commit()
        return service
    except:
        session.rollback()
        raise

def get_all_employees(session , serviceID):
    return get_employees_by_service(session = session , serviceID=serviceID)

def delete_service(session, serviceID):
    try:
        if get_service(serviceID=serviceID, session=session)[0] == 'FAIL':
            raise NotFoundService()

        active_appointments = session.query(AppointmentService).filter(
            AppointmentService.service_id == serviceID,
            AppointmentService.status.in_([AppointmentStatus.PENDING, AppointmentStatus.CONFIRMED])
        ).first()
        if active_appointments is not None:
            raise ServiceHasHistory()  # add this exception to app/exceptions/service.py

        del_employee_by_service(session=session, serviceID=serviceID)
        del_appointment_by_service(session=session, serviceID=serviceID)  # cleans up any COMPLETED/CANCELLED rows if you want them removed too
        del_service(session=session, serviceID=serviceID)
        session.commit()
    except:
        session.rollback()
        raise

# def reprice_service(session , serviceID , newPrice):
#     try:
#         service =get_or_raise(session=session,serviceID=serviceID)
#         service[1].price = newPrice
#         session.commit()
#     except:
#         session.rollback()
#         raise

# def rename_service (session , serviceID , newDescription):
#     try:
#         service = get_or_raise(session=session,serviceID=serviceID)
#         if (get_service_by(session=session , category=service[1].category , desricption=newDescription)[0] == 'OK'):
#             raise DuplicateService()
#         service[1].description= newDescription.upper()
#         session.commit()
#     except:
#         session.rollback()
#         raise

    
# def change_time_service (session , serviceID , newTime):
#     try:
#         service = get_or_raise(session=session,serviceID=serviceID)
#         service[1].time_duration = newTime 
#         session.commit()
#     except:
#         session.rollback()
#         raise

def alter_service(session , serviceID , data):
    try:
        service = get_or_raise(session=session , serviceID = serviceID)
        for field, value in data.model_dump(exclude_unset = True).items():
            if (field == 'description'):
                value = value.upper()
            setattr(service,field,value)
        session.commit()
        session.refresh(service)
        return service
    except:
        session.rollback()
        raise

def activate_service (session , serviceID):
    try:
        service = get_or_raise(session=session,serviceID=serviceID)
        service.active = True
        session.commit()
    except:
        session.rollback()
        raise

def deactivate_service (session , serviceID):
    try:
        service = get_or_raise(session=session,serviceID=serviceID)
        service.active = False
        session.commit()
    except:
        session.rollback()
        raise

def pick_employee_service(session , employeeID,serviceID):
        employee_service = get_employee_service(session=session,employeeID=employeeID,serviceID=serviceID)
        if (employee_service[1] is None):
            raise EmployeeNotAssigned()
        return employee_service[1]
