from app.database import SessionLocal
from app.auth.google import oauth
from fastapi import Request , HTTPException , Depends
from starlette.responses import RedirectResponse
from app.CRUD.user import get_user
from app.enums.enum import Role
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_google_user(request: Request):
    user_id = request.session.get('user_id')
    if not user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user_id

async def get_current_user(userID: int = Depends(get_google_user), db: dict = Depends(get_db)):
    status, user = get_user(session=db, userID=userID)
    if status == 'FAIL':
        raise HTTPException(status_code=401, detail="User not found")
    return user

def require_admin(user : dict = Depends(get_current_user)):
    if (user.role != Role.ADMIN):
        raise HTTPException(status_code=403 , detail= "You are not allowed")

    
def require_self_receptionist_or_admin(employeeID: int,user: dict = Depends(get_current_user)):
    if user.role == Role.EMPLOYEE:
        if user.employee_id != employeeID:
            raise HTTPException(
                status_code=403,
                detail="You are not allowed"
            )
        return user

    if user.role in [Role.ADMIN, Role.RECEPTION]:
        return user

    raise HTTPException(status_code=403,detail="You are not allowed")

def require_receptionist_or_admin(user: dict = Depends(get_current_user)):
    if user.role in [Role.ADMIN, Role.RECEPTION]:
        return user
    raise HTTPException(status_code=403,detail="You are not allowed")