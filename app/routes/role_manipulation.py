from fastapi import Depends , APIRouter , HTTPException

from app.business.role_logic import *
from app.dependencies import require_admin , get_db , get_current_user
from app.schemas.employee import EmployeeResponse

router = APIRouter(prefix='/role' , tags=['role-manipulation'])

@router.post('/make_employee/{userID}' , dependencies=[Depends(require_admin)],summary='Add new employee' )
def add_employee(userID : int, phone:str, db :dict = Depends(get_db) , user : dict = Depends(get_current_user)):
        try:    
            return make_employee(session=db ,current_user=user ,userID=userID,phone = phone)
        except IsNotAdmin:
            raise HTTPException(status_code=403 , detail='You are not allowed')
        except IsClient:
            raise HTTPException(status_code=400 , detail='User is client')   
        except EmployeeHasHistory:
            raise HTTPException(status_code=400 , detail= 'Employee has live appointments')
        except NotFound:
            raise HTTPException(status_code=404 , detail='Employee not found')
        except IsEmployee:
            raise HTTPException(status_code=400 , detail='User is employee')
        except InvalidPhoneNumber:
            raise HTTPException(status_code=403 , detail='Invalid phone number')



             

@router.delete('/delete_employee/{userID}' , dependencies=[Depends(require_admin)],summary='Delete employee' )
def destroy_employee(userID : int, db :dict = Depends(get_db) , user : dict = Depends(get_current_user)):
        try:    
            return delete_employee(session=db ,current_user=user ,userID=userID)
        except IsNotAdmin:
            raise HTTPException(status_code=403 , detail='You are not allowed')
        except IsClient:
            raise HTTPException(status_code=400 , detail='User is client')   
        except EmployeeHasHistory:
            raise HTTPException(status_code=400 , detail= 'Employee has live appointments')
        except NotFound:
            raise HTTPException(status_code=404 , detail='Employee not found')

@router.put('/make_receptionist/{userID}' , dependencies=[Depends(require_admin)],summary='Add new receptionist' )
def add_receptionist(userID : int, db :dict = Depends(get_db) , user : dict = Depends(get_current_user)):
        try:    
            return make_receptionist(session=db ,current_user=user ,userID=userID)
        except IsNotAdmin:
            raise HTTPException(status_code=403 , detail='You are not allowed')
        except IsClient:
            raise HTTPException(status_code=400 , detail='User is client')   
        except NotFound:
            raise HTTPException(status_code=404 , detail='Employee not found')

@router.delete('/delete_receptionist/{userID}' , dependencies=[Depends(require_admin)],summary='Delete receptionist' )
def destroy_receptionist(userID : int, db :dict = Depends(get_db) , user : dict = Depends(get_current_user)):
        try:    
            return delete_receptionist(session=db ,current_user=user ,userID=userID)
        except IsNotAdmin:
            raise HTTPException(status_code=403 , detail='You are not allowed')
        except IsClient:
            raise HTTPException(status_code=400 , detail='User is client')   
        except NotFound:
            raise HTTPException(status_code=404 , detail='Employee not found')

@router.put('/make_admin/{userID}' , dependencies=[Depends(require_admin)],summary='Add new admin' )
def add_admin(userID : int, db :dict = Depends(get_db) , user : dict = Depends(get_current_user)):
        try:    
            return make_admin(session=db ,current_user=user ,userID=userID)
        except IsNotAdmin:
            raise HTTPException(status_code=403 , detail='You are not allowed')
        except IsClient:
            raise HTTPException(status_code=400 , detail='User is client')   
        except NotFound:
            raise HTTPException(status_code=404 , detail='Employee not found')

@router.delete('/delete_admin/{userID}' , dependencies=[Depends(require_admin)],summary='Delete admin' )
def destroy_admin(userID : int, db :dict = Depends(get_db) , user : dict = Depends(get_current_user)):
        try:    
            return delete_admin(session=db ,current_user=user ,userID=userID)
        except IsNotAdmin:
            raise HTTPException(status_code=403 , detail='You are not allowed')
        except IsClient:
            raise HTTPException(status_code=400 , detail='User is client')   
        except NotFound:
            raise HTTPException(status_code=404 , detail='Employee not found')