from fastapi import APIRouter, Depends ,HTTPException

from app.schemas.user import *
from app.dependencies import get_db , get_google_user , require_receptionist_or_admin
from app.CRUD.user import get_user 
from app.CRUD.user import get_all_users as crud_all_users

from app.business.user import *
from app.exceptions.user import *
from starlette.responses import RedirectResponse
router = APIRouter(prefix='/user',tags=['user'])

@router.get('/me',response_model= UserResponse)
def me(db:dict = Depends(get_db) , userID :int =Depends(get_google_user)):
    status, user = get_user(session=db , userID=userID)
    if (status == 'FAIL'):
        raise HTTPException(status_code=404 , detail='Not found')
    return user

@router.post('/rename' )
def rename(data:RenameUserRequest,db:dict = Depends(get_db),userID : int = Depends(get_google_user)):
    rename_user(session=db , userID=userID,f_name=data.f_name,l_name = data.l_name)

@router.get('/all' , dependencies=[Depends(require_receptionist_or_admin)],summary='Get all users')
def all_users(db:dict = Depends(get_db)):
    return crud_all_users(session=db)

@router.post('/update-phone')
def update_phone_route(data: PhoneUpdateRequest, db: dict = Depends(get_db), userID: int = Depends(get_google_user)):
    try:
        return update_phone(session=db, userID=userID, phone=data.phone)
    except InvalidPhoneNumber:
        raise HTTPException(status_code=400, detail="Invalid phone number")
    except UsedPhoneNumber:
        raise HTTPException(status_code=409, detail="This phone number is already in use")