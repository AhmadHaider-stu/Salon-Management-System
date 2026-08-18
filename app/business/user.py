from app.CRUD.user import * 
from app.CRUD.employee import get_employee , update_employee_name
from app.CRUD.client import get_client, update_client
from app.exceptions.user import *


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
