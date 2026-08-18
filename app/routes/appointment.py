from fastapi import APIRouter , HTTPException , Depends

from app.schemas.appointment import AppointmentCreate , AppointmentStatus , RescheduleRequest , AddServiceRequest , PriceUpdateRequest
from app.dependencies import get_db , get_current_user , require_receptionist_or_admin

from app.business.appointment_logic import book_appointment , change_appointment_status , delete_appointment_service , delete_appointment , reschedule_appointment , add_service_to_appointment , update_appointment_service_price
from app.business.appointment_logic import get_or_raise as appointment_get_or_raise

from app.CRUD.appointment import get_client_appointment
from app.CRUD.appointment_service import get_appointment_service_by_appointment 
from app.enums.enum import Role
from app.exceptions.employee import *
from app.exceptions.client import *
from app.exceptions.user import IsBlocked
from app.exceptions.service import *
from app.exceptions.appointments import *

from app.business.client_logic import find_or_create_walk_in
from app.schemas.client import WalkInBookingCreate



router = APIRouter(prefix='/appointment', tags=['appointment'])

def check_appointment_ownership(appointment , user):
    if (user.role in [Role.ADMIN , Role.RECEPTION]):
        return True
    if (user.client_id != appointment.client_id):
        return False
    return True

@router.get('' , summary='list all my appointments')
def list_my_appointments(db:dict = Depends(get_db) , user = Depends(get_current_user)):
    if (user.client_id == None):
        raise HTTPException(status_code=403 ,detail='No client record for user' )
    return get_client_appointment(session=db , clientID=user.client_id)

@router.get('/{appointmentID}' , summary='Get specific appointment')
def get_this_appointment(appointmentID : int , db:dict = Depends(get_db) , user:dict = Depends(get_current_user)):
    try:
        appointment = appointment_get_or_raise(session=db , appointmentID=appointmentID)
        if (not check_appointment_ownership(appointment=appointment , user=user)):
            raise HTTPException(status_code=403 , detail='You are not allowed')
        services_status , services = get_appointment_service_by_appointment(session=db , appointmentID=appointmentID)
        return{"appointment": appointment , "services" : services if services_status == 'OK' else []}
    except NotFoundAppointment:
        raise HTTPException(status_code=404 , detail = 'Appointment not found')
    

@router.post('' , summary='Book an appointment')
def create_appointment(data: AppointmentCreate, db: dict = Depends(get_db), user=Depends(get_current_user)):
    if user.client_id is None:
        raise HTTPException(status_code=403, detail="No client record for this user")
    try:
        appointment = book_appointment(
            session=db,
            clientID=user.client_id,
            employee_servicesIDs=data.services,
            start_time=data.start_time,
            note = data.note
        )
    except InvalidPhoneNumber:
        raise HTTPException(status_code=400, detail="Invalid phone number")
    except NotFoundService:
        raise HTTPException(status_code=404, detail="One of the selected services was not found")
    except NotFoundEmployee:
        raise HTTPException(status_code=404, detail="Employee not found")
    except InactiveEmployee:
        raise HTTPException(status_code=400, detail="Employee is not active")
    except EmployeeNotAssigned:
        raise HTTPException(status_code=400, detail="Employee not assigned to this service")
    except EmployeeBusy:
        raise HTTPException(status_code=409, detail="Employee is not available at this time")
    except DoubleBook:
        raise HTTPException(status_code=409, detail="You already have an active appointment")
    except IsBlocked:
        raise HTTPException(status_code=403, detail="Account is blocked")
    except NotFoundClient:
        raise HTTPException(status_code=404, detail="Client not found")

    return{"appointment": appointment , "services" : data.services}
        
@router.put('/{appointmentID}/status' , summary ='Change appointment status' , dependencies=[Depends(require_receptionist_or_admin)])
def change_status(status : AppointmentStatus,appointmentID : int , db : dict = Depends(get_db)):
    try:
        change_appointment_status(session=db ,appointmentID=appointmentID,status= status)
        return 'Status changed'
    except NotFoundAppointment:
        HTTPException(status_code=404 , detail = 'Not found appointment')

@router.delete('/appointment_service/{appointmentServiceID:int}' , summary= 'Delete appointment service' , dependencies=[Depends(require_receptionist_or_admin)])
def cancel_appointment_service(appointmentServiceID,db:dict = Depends(get_db)):
    try :
        last_service = delete_appointment_service(session=db , appointment_serviceID=appointmentServiceID)
        return last_service
    except NotFoundAppointment:
        HTTPException(status_code=404 , detail = 'Not found appointment')

@router.delete('/{appointmentID}' , summary = 'Delete appointment' , dependencies=[Depends(require_receptionist_or_admin)])
def destroy_appointment(appointmentID:int , db:dict = Depends(get_db)):
    try:
        delete_appointment(session = db , appointmentID=appointmentID)
        return 'OK'
    except NotFoundAppointment:
        raise HTTPException(status_code=404,detail= 'Not found appointment')



@router.post('/walk-in', summary='Book an appointment for a walk-in client', dependencies=[Depends(require_receptionist_or_admin)])
def create_walk_in_appointment(data: WalkInBookingCreate, db: dict = Depends(get_db)):
    try:
        client = find_or_create_walk_in(
            session=db,
            f_name=data.client.f_name,
            l_name=data.client.l_name,
            phone=data.client.phone,
            email=data.client.email,
        )
        appointment = book_appointment(
            session=db,
            clientID=client.id,
            employee_servicesIDs=data.services,
            start_time=data.start_time,
        )
    except InvalidPhoneNumber:
        raise HTTPException(status_code=400, detail="Invalid phone number")
    except NotFoundService:
        raise HTTPException(status_code=404, detail="One of the selected services was not found")
    except NotFoundEmployee:
        raise HTTPException(status_code=404, detail="Employee not found")
    except InactiveEmployee:
        raise HTTPException(status_code=400, detail="Employee is not active")
    except EmployeeNotAssigned:
        raise HTTPException(status_code=400, detail="Employee not assigned to this service")
    except EmployeeBusy:
        raise HTTPException(status_code=409, detail="Employee is not available at this time")
    except DoubleBook:
        raise HTTPException(status_code=409, detail="This client already has an active appointment")
    except IsBlocked:
        raise HTTPException(status_code=403, detail="Account is blocked")
    except NotFoundClient:
        raise HTTPException(status_code=404, detail="Client not found")

    return {"appointment": appointment, "client": client}



@router.put('/{appointmentID}/reschedule', dependencies=[Depends(require_receptionist_or_admin)])
def reschedule(appointmentID: int, data: RescheduleRequest, db: dict = Depends(get_db)):
    try:
        return reschedule_appointment(session=db, appointmentID=appointmentID, new_start_time=data.start_time)
    except NotFoundAppointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    except CannotModifyAppointment:
        raise HTTPException(status_code=400, detail="Cannot modify a completed or cancelled appointment")
    except EmployeeBusy:
        raise HTTPException(status_code=409, detail="Employee is not available at this time")
    except DoubleBook:
        raise HTTPException(status_code=409, detail="Client already has an active appointment")


@router.post('/{appointmentID}/services', dependencies=[Depends(require_receptionist_or_admin)])
def add_service(appointmentID: int, data: AddServiceRequest, db: dict = Depends(get_db)):
    try:
        return add_service_to_appointment(session=db, appointmentID=appointmentID,
                                           employeeID=data.employee_id, serviceID=data.service_id)
    except NotFoundAppointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    except CannotModifyAppointment:
        raise HTTPException(status_code=400, detail="Cannot modify a completed or cancelled appointment")
    except NotFoundService:
        raise HTTPException(status_code=404, detail="Service not found")
    except EmployeeNotAssigned:
        raise HTTPException(status_code=400, detail="Employee not assigned to this service")
    except EmployeeBusy:
        raise HTTPException(status_code=409, detail="Employee is not available at this time")


@router.put('/appointment_service/{appointmentServiceID}/price', dependencies=[Depends(require_receptionist_or_admin)])
def edit_price(appointmentServiceID: int, data: PriceUpdateRequest, db: dict = Depends(get_db)):
    try:
        return update_appointment_service_price(session=db, appointmentServiceID=appointmentServiceID, new_price=data.price)
    except NotFoundAppointment:
        raise HTTPException(status_code=404, detail="Appointment service not found")
    except CannotModifyAppointment:
        raise HTTPException(status_code=400, detail="Cannot modify a completed or cancelled appointment")