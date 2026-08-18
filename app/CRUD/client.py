from app.models.client import *

# Adding and removing clients -- improve it to a new column (isActive)

def add_client (session , f_name,l_name , email , phone ):
    new_client = Client(f_name = f_name , l_name = l_name , email = email , phone = phone)
    session.add(new_client)
    session.flush()
    return new_client

def del_client(session , clientID):
    client = get_client(session=session,clientID=clientID)
    session.delete(client[1])
    return 'OK'


def get_client_by_email(session , email):
    client = session.query(Client).filter(Client.email==email).one_or_none()
    if (client == None):
        return 'FAIL',None
    return 'OK',client

def get_client_by_phone(session , phone):
    client = session.query(Client).filter(Client.phone==phone).one_or_none()
    if (client == None):
        return 'FAIL',None
    return 'OK',client

def get_client(session , clientID):
    client = session.query(Client).filter(Client.id==clientID).one_or_none()
    if (client == None):
        return 'FAIL',None
    return 'OK',client
# args[0] and args[1] attribute, args[2] and args[3] in case of name changing 
def update_client (session , client , *args):
    if (len(args)>3):
        client.f_name=args[2].upper()
        client.l_name=args[3].upper()
    session.flush()

def get_all_clients(session):
    clients = session.query(Client).all()
    return clients