from app.CRUD.client import *
from app.exceptions.client import *
from app.models.appointment import *
from app.CRUD.user import *
from app.services.phone_validation import is_valid_phone, format_phone
from app.models.appointment import *

def get_or_raise(session , clientID):
        status, client = get_client(session=session,clientID=clientID)
        if (status == 'FAIL'):
                raise NotFoundClient()
        return client
        
def register_client (session , f_name , l_name ,phone, email= None ):
        f_name = f_name.upper()
        l_name = l_name.upper()
        if phone is not None and not is_valid_phone(phone, "JO"):
                raise InvalidPhoneNumber()      
        if phone is not None:
                phone = format_phone(phone, "JO")
        client = add_client(session=session, f_name=f_name, l_name=l_name, email=email, phone=phone)
        return client

def delete_client(session, clientID):
        try:
                status, client = get_client(session=session, clientID=clientID)
                if status == 'FAIL':
                        raise NotFoundClient()

                active_appointments = session.query(Appointment).filter(
                Appointment.client_id == clientID,
                Appointment.status.in_([AppointmentStatus.PENDING, AppointmentStatus.CONFIRMED])
                ).first()
                if active_appointments is not None:
                        raise ClientHasHistory()

                status_u, user = get_user_by_client(session=session, clientID=clientID)  # CONFIRM: does this CRUD function exist?
                if status_u == 'OK':
                        raise ClientHasAccount()  # new exception — don't delete a client who has a linked User account

                del_client(session=session, clientID=clientID)
                session.commit()
                return 'OK'
        except:
                session.rollback()
                raise

def find_or_create_walk_in(session, f_name, l_name, phone, email=None):
        try:
                if not is_valid_phone(phone, "JO"):
                        raise InvalidPhoneNumber()
                formatted_phone = format_phone(phone, "JO")

                status, existing = get_client_by_phone(session=session, phone=formatted_phone)
                if status == 'OK':
                        return existing
                return register_client(session=session, f_name=f_name, l_name=l_name, phone=formatted_phone, email=email)
        except:
                session.rollback()
                raise

def alter_client (session, clientID , data):
        try:
                client = get_or_raise(session=session, clientID=clientID)
                updates = data.model_dump(exclude_unset=True)

                if 'phone' in updates:
                        if not is_valid_phone(updates['phone'], "JO"):
                                raise InvalidPhoneNumber()
                        updates['phone'] = format_phone(updates['phone'], "JO")

                for field, value in updates.items():
                        if field in ('f_name', 'l_name'):
                                value = value.upper()
                        setattr(client, field, value)
                session.commit()
                session.refresh(client)
                return client
        except:
                session.rollback()
                raise

def get_appointments_by_client(session , clientID):
        try:
                get_or_raise(session=session, clientID=clientID)
                query = session.query(Appointment).filter(Appointment.client_id == clientID).all()
                return query
        except:
                session.rollback()
                raise