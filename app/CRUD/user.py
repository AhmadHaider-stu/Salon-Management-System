from app.models.user import *

def add_user (session , f_name , l_name , sub , email , role ,phone, provider=None):
    new_user = User(f_name = f_name , l_name = l_name , email = email,phone = phone , role = role, oauth_sub = sub )
    
    session.add(new_user)
    session.flush()
    return new_user

def get_user(session, userID):
    user  = session.query(User).filter(User.id == userID).one_or_none()
    if user == None:
        return 'FAIL',None
    return 'OK',user

def get_user_by_email(session, email):
    user  = session.query(User).filter(User.email == email).one_or_none()
    if user == None:
        return 'FAIL',None
    return 'OK',user

def del_user(session, userID):
    status, user = get_user(session=session, userID=userID)
    if status == 'FAIL':
        return 'FAIL'
    session.delete(user)
    session.flush()
    return 'OK'

# args[0] = attribute , args[1] , args[2] in case of names 

def update_user (session , user ,*args ):  
    user.f_name = args[2].upper()
    user.l_name = args[3].upper()
    session.flush()


def block_user(session , user):
    user.block = 1
    session.flush()

def unblock_user (session,user):
    user.block = 0
    session.flush()

def get_all_users(session):
    users = session.query(User).all()
    return users

def get_user_by_sub(session , sub):
    user = session.query(User).filter(User.oauth_sub == sub).one_or_none()
    return user

def get_user_by_client(session , clientID):
    user = session.query(User).filter(User.client_id== clientID).one_or_none()
    return user

def get_user_by_phone(session, phone):
    user = session.query(User).filter(User.phone == phone).one_or_none()
    if user is None:
        return 'FAIL', None
    return 'OK', user
def get_employees(session):
    return session.query(User).filter(User.role == Role.EMPLOYEE).all()
