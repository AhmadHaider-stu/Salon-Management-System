from fastapi import APIRouter, Depends, HTTPException

from app.schemas.service import *
from app.dependencies import get_db , get_google_user , require_admin
from app.business.service_logic import *
from app.exceptions.service import *
from app.CRUD.user import get_user
from app.CRUD.employee_service import get_employees_by_service

router = APIRouter(prefix='/service',tags=['service'])

@router.post('/add_service' , response_model=ServiceResponse , description="Adding new service", dependencies=[Depends(require_admin)])
def add_service(data : ServiceCreate ,db:dict = Depends(get_db)):
    try:
        service = create_service(session=db,
                                category=data.category ,
                                description=data.description,
                                price=data.price,
                                time_duration=data.time_duration)
    except DuplicateService:
        raise HTTPException(status_code=409, detail="Service already exists")
    return service
    
@router.get('/all' , description='Get all created services')
def list_services(db:dict = Depends(get_db) , category:ServiceCategory =None):
    services = get_services(session = db,category=category)
    return services


@router.get('/{serviceID}/employees' , description='Get all employees for service')
def list_employees_service(serviceID : int,db:dict = Depends(get_db)):
    employees = get_employees_by_service(session=db,serviceID=serviceID)
    return employees


@router.get("/{serviceID}" , summary='Get specific service' , dependencies=[Depends(require_admin)] ,response_model=ServiceResponse)
def service(serviceID:int,db:dict = Depends(get_db)):
    status ,service = get_service(session=db , serviceID = serviceID)
    if (status == 'FAIL'):
        raise HTTPException(status_code=404 , detail='Service not found')
    return service

@router.put('/{serviceID}',summary='Edit specific service' , dependencies=[Depends(require_admin)] , response_model=ServiceResponse)
def edit_service(data:ServiceUpdate,serviceID:int,db:dict = Depends(get_db)):
    try:
        return alter_service(session=db, serviceID=serviceID, data=data)
    except NotFoundService:
        raise HTTPException(status_code=404, detail="Service not found")

@router.delete('/{serviceID}',summary='Delete specific service' , dependencies=[Depends(require_admin)])
def destroy_service(serviceID:int,db:dict = Depends(get_db)):
    try:
        delete_service(session=db, serviceID=serviceID)
    except NotFoundService:
        raise HTTPException(status_code=404, detail="Service not found")
    return 'OK'

