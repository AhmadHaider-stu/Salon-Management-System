from app.CRUD.user import *
from app.exceptions.user import *
from app.CRUD.client import get_client
from app.business.client_logic import register_client
from app.services.phone_validation import is_valid_phone, format_phone


def register_user(session, f_name, oauth_sub, l_name, email, phone, provider=None):
    try:
        isExist = get_user_by_sub(session=session, sub=oauth_sub)
        if isExist is not None:
            if isExist.block == 1:
                raise IsBlocked()
            return login_user(session=session, oauth_sub=oauth_sub)

        if not is_valid_phone(phone, "JO"):
            raise InvalidPhoneNumber()
        phone = format_phone(phone, "JO")

        status, existing_phone_user = get_user_by_phone(session=session, phone=phone)  # CONFIRM: need this CRUD function
        if status == 'OK':
            raise UsedPhoneNumber()
        f_name = f_name.upper()
        l_name = l_name.upper()
        user = add_user(session=session, f_name=f_name, l_name=l_name, email=email, role=Role.CLIENT, sub=oauth_sub, phone=phone)
        client = register_client(session=session, f_name=user.f_name, l_name=user.l_name, phone=phone, email=user.email)
        user.client_id = client.id
        session.commit()
        return user
    except:
        session.rollback()
        raise

def login_user (session , oauth_sub):
        user = get_user_by_sub(session=session, sub = oauth_sub)
        if (user == None):
             raise NotFound()
        if (user.block == 1):
             raise IsBlocked()
        return user

def complete_phone(session, userID, phone):
    try:
        status, user = get_user(session=session, userID=userID)
        if status == 'FAIL':
            raise NotFound()
        if not is_valid_phone(phone, "JO"):
            raise InvalidPhoneNumber()
        phone = format_phone(phone, "JO")

        user.phone = phone
        if user.client_id is not None:
            status_c, client = get_client(session=session, clientID=user.client_id)
            if status_c == 'OK':
                client.phone = phone

        session.commit()
        return user
    except:
        session.rollback()
        raise


