from app.models.employee_service import *
from app.models.employee import *
from app.models.service import *


def add_employee_service (session , employeeID , servicesID):
    for serviceID in servicesID:
        new_employee_service = EmployeeService(employee_id = employeeID , service_id = serviceID)
        session.add(new_employee_service)
    return 'OK'

def get_services_by_employee(session, employeeID):
    links = session.query(EmployeeService).filter(EmployeeService.employee_id == employeeID).all()
    service_ids = [link.service_id for link in links]
    services = session.query(Service).filter(Service.id.in_(service_ids), Service.active == True).all()
    return services

def get_employees_by_service(session, serviceID):
    links = session.query(EmployeeService).filter(EmployeeService.service_id == serviceID).all()
    employee_ids = [link.employee_id for link in links]
    employees = session.query(Employee).filter(Employee.id.in_(employee_ids), Employee.active == True).all()
    return employees

def get_employee_service(session , employeeID , serviceID):
    employee_service = session.query(EmployeeService).filter(EmployeeService.service_id == serviceID,
                                                             EmployeeService.employee_id == employeeID).one_or_none()
    if (employee_service == None):
        return 'FAIL',None
    return 'OK',employee_service

def del_services_employee(session, employeeID,servicesID):
    services = session.query(EmployeeService).filter(EmployeeService.service_id.in_(servicesID) , EmployeeService.employee_id==employeeID)
    for row in services:
        session.delete(row)
    session.flush()

def del_employee_by_service(session , serviceID):
    services = session.query(EmployeeService).filter(EmployeeService.service_id == serviceID).all()
    for row in services:
        session.delete(row)
    session.flush()

def del_service_by_employee(session, employeeID):
    services = session.query(EmployeeService).filter(EmployeeService.employee_id == employeeID).all()
    for row in services:
        session.delete(row)
    session.flush()