from app.CRUD.user import * 
from app.CRUD.employee import get_employee , update_employee_name
from app.CRUD.client import get_client, update_client
from app.exceptions.user import *
from app.services.phone_validation import is_valid_phone, format_phone


#RENAME 

def rename_user(session , userID , f_name, l_name):
    f_name = f_name.upper()
    l_name = l_name.upper()
    try :
        user = get_user(session=session,userID= userID)
        if (user[0]== 'FAIL'):
            raise NotFound()
        user[1].f_name = f_name
        user[1].l_name = l_name

        if (user[1].role != Role.CLIENT):
            employee = get_employee(session=session,employeeID=user[1].employee_id)
            if(employee[0]=='FAIL'):
                raise NotFound()
            update_employee_name(session ,employee[1] ,f_name , l_name)
        else:
            client = get_client(session=session,clientID=user[1].client_id)
            if (client[0]=='FAIL'):
                raise NotFound()
            update_client(session , client[1] , 'f_name' , 'l_name' , f_name , l_name)
        session.commit()
    except:
        session.rollback()
        raise

def update_phone(session, userID, phone):
    try:
        status, user = get_user(session=session, userID=userID)
        if status == 'FAIL':
            raise NotFound()

        if not is_valid_phone(phone, "AE"):
            raise InvalidPhoneNumber()
        phone = format_phone(phone, "AE")

        status_p, existing = get_user_by_phone(session=session, phone=phone)
        if status_p == 'OK' and existing.id != user.id:
            raise UsedPhoneNumber()

        user.phone = phone

        if user.client_id is not None:
            status_c, client = get_client(session=session, clientID=user.client_id)
            if status_c == 'OK':
                client.phone = phone

        if user.employee_id is not None:
            status_e, employee = get_employee(session=session, employeeID=user.employee_id)
            if status_e == 'OK':
                employee.phone = phone

        session.commit()
        return user
    except:
        session.rollback()
        raise