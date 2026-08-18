from fastapi import APIRouter , Depends , HTTPException , UploadFile, File

from app.schemas.employee import *
from app.schemas.employee_schedule import *
from app.dependencies import get_db  , require_self_receptionist_or_admin , require_receptionist_or_admin 
from app.business.employee_logic import *

from app.business.service_logic import get_services_by_employee 
from app.business.service_logic import get_or_raise as service_get_or_raise 

from app.exceptions.service import NotFoundService

from app.business.employee_schedule import set_employee_schedule
from app.CRUD.employee_schedule import get_schedule_for_employee as crud_employee_schedule
from app.exceptions.employee_schedule import InvalidScheduleTime
from app.CRUD.employee import get_employees 
from app.CRUD.employee import get_employee as crud_get_employee 
from app.CRUD.appointment_service import get_employee_appointments as crud_get_employee_appointments


from datetime import date as date_type
from app.business.calendar_logic import get_employee_calendar_day, get_employee_calendar_month
from app.dependencies import get_current_user
from app.enums.enum import Role


router = APIRouter(prefix='/employee' ,tags=['employee'])

@router.get('/all',dependencies=[Depends(require_receptionist_or_admin)] )
def get_all_employees(db : dict = Depends(get_db)):
    return get_employees(session=db)

@router.get('/{employee_id}',dependencies=[Depends(require_receptionist_or_admin)] , summary='Get specific employee' ,  response_model=EmployeeResponse)
def get_employee(employeeID:int,db:dict = Depends(get_db)):
    status, employee = crud_get_employee(session = db,employeeID=employeeID)
    if (status == 'FAIL'):
        raise HTTPException(status_code=404 , detail= 'Employee not found')
    return employee

@router.get('/{employeeID}/services' , dependencies=[Depends(require_receptionist_or_admin)], summary="Get employee's services")
def get_employee_services(employeeID:int , db:dict = Depends(get_db)):
    status, employee = crud_get_employee(session = db,employeeID=employeeID)
    if (status == 'FAIL'):
        raise HTTPException(status_code=404 , detail= 'Employee not found')
    services = get_services_by_employee(session=db , employeeID=employee.id)
    return services


@router.get('/{employeeID}/schedule', dependencies=[Depends(require_self_receptionist_or_admin)], summary='Get weekly schedule')
def get_employee_schedule(employeeID : int , db:dict = Depends(get_db)):
    status, employee = crud_get_employee(session = db,employeeID=employeeID)
    if (status == 'FAIL'):
        raise HTTPException(status_code=404 , detail= 'Employee not found')
    schedule = crud_employee_schedule(session=db ,employee_id= employeeID)
    return schedule

@router.get('/{employeeID}/appointments' , dependencies=[Depends(require_self_receptionist_or_admin)],summary = "Get employee's appointments")
def get_employee_appointments(employeeID:int , db:dict = Depends(get_db)):
    status, employee = crud_get_employee(session = db,employeeID=employeeID)
    if (status == 'FAIL'):
        raise HTTPException(status_code=404 , detail= 'Employee not found')
    appointments = crud_get_employee_appointments(session=db , employeeID=employee.id)
    return appointments


@router.post('/{employeeID}/assign_services' , dependencies=[Depends(require_receptionist_or_admin)],summary = 'Assign services to employee')
def add_employee_services(data:EmployeeServicesRequest,employeeID : int , db:dict = Depends(get_db)):
    try:
        for service in data.services:
            service_get_or_raise(session=db , serviceID=service)
        assign_employee_services(session = db , employeeID=employeeID ,servicesID =data.services)
        return 'OK'
    except NotFoundEmployee:
        raise HTTPException(status_code=404 , detail = 'Employee not found')
    except NotFoundService:
        raise HTTPException(status_code=404 , detail = 'Service not found')

@router.put('/{employeeID}/schedule' , summary = 'Set the work days for employee' , dependencies=[Depends(require_self_receptionist_or_admin)])
def set_schedule(employeeID : int ,data: EmployeeScheduleUpdate, db : dict = Depends(get_db)):
    try:
        entries = [entry.model_dump() for entry in data.entries]
        set_employee_schedule(session=db , employee_id=employeeID , schedule_list= entries)
    except InvalidScheduleTime:
        raise HTTPException(status_code=400, detail="End time must be after start time")
    return {'detail' : 'Schedule updated'}


@router.put('/{employeeID}', summary='Edit specific employee', dependencies=[Depends(require_self_receptionist_or_admin)], response_model=EmployeeResponse)
def edit_employee(data: EmployeeUpdate, employeeID: int, db: dict = Depends(get_db)):
    try:
        return alter_employee(session=db, employeeID=employeeID, data=data)
    except NotFoundEmployee:
        raise HTTPException(status_code=404, detail="Employee not found")
    except InvalidPhoneNumber:
        raise HTTPException(status_code=400, detail="Invalid phone number")

@router.put('/{employeeID}/photo', dependencies=[Depends(require_self_receptionist_or_admin)])
def upload_employee_photo(employeeID: int, file: UploadFile = File(...), db: dict = Depends(get_db)):
    try:
        url = update_employee_photo_upload(session=db, employeeID=employeeID, file=file)
        return {"photo_url": url}
    except NotFoundEmployee:
        raise HTTPException(status_code=404, detail="Employee not found")

@router.get('/{employeeID}/calendar/day')
def employee_calendar_day(employeeID: int, date: date_type, db: dict = Depends(get_db), user=Depends(get_current_user)):
    if user.role not in (Role.ADMIN, Role.RECEPTION) and user.employee_id != employeeID:
        raise HTTPException(status_code=403, detail="You are not allowed")
    return get_employee_calendar_day(session=db, employeeID=employeeID, date=date, viewer=user)


@router.get('/{employeeID}/calendar/month')
def employee_calendar_month(employeeID: int, year: int, month: int, db: dict = Depends(get_db), user=Depends(get_current_user)):
    if user.role not in (Role.ADMIN, Role.RECEPTION) and user.employee_id != employeeID:
        raise HTTPException(status_code=403, detail="You are not allowed")
    return get_employee_calendar_month(session=db, employeeID=employeeID, year=year, month=month, viewer=user)