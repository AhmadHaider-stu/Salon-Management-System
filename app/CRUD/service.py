from app.models.service import *

def add_service(session, category, description, price, time_duration, active=True):
    description = description.upper()
    isDup = get_service_by(session=session, category=category, description=description)
    if isDup[0] == 'OK':
        return "FAIL", None
    new_service = Service(category=category, description=description, price=price, active=active, time_duration=time_duration)
    session.add(new_service)
    session.flush()
    return "OK", new_service

def del_service(session, serviceID):
    result = get_service(session=session, serviceID=serviceID)
    if result[0] == 'FAIL':
        return 'FAIL', None
    session.delete(result[1])
    session.flush()
    return 'OK', None


def get_service(session , serviceID):
    service = session.query(Service).filter(Service.id == serviceID).one_or_none()
    if (service != None):
        return 'OK',service
    return 'FAIL',None

def get_service_by (session , category , description):
    service = session.query(Service).filter(Service.category == category , Service.description == description).one_or_none()
    if service == None:
        return 'FAIL',None
    return 'OK',service

def get_services(session , category = None):
    services = session.query(Service)
    if (category != None):
        services = services.filter(Service.category == category)
    return services.all()

