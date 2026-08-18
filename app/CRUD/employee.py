from app.models.employee import Employee


# Add new Employee all the non required parameters are given default value
def add_employee(session, f_name ,l_name, email , phone, photo = None , socialMedia = None , active = True ):
    new_employee = Employee(f_name = f_name , l_name = l_name ,phone = phone, email = email , photo = photo, socialMedia = socialMedia , active = active)
    session.add(new_employee)
    session.flush()
    return new_employee

# These functions are displayed only for ADMIN 
# ==================================================

def del_employee(session , employee):
    session.delete(employee)
    session.flush()
    return "OK" 

# ==================================================

# Get employee by email

def get_employee_by_email(session , email):
    employee = session.query(Employee).filter(Employee.email == email).one_or_none()
    if employee == None:
        return 'FAIL',None
    return 'OK',employee

def get_employee(session , employeeID):
    employee = session.query(Employee).filter(Employee.id == employeeID).one_or_none()
    if employee == None:
        return 'FAIL',None
    return 'OK',employee

def get_employees(session ):
    employees = session.query(Employee).all()
    return employees
# Update the employee data only avaiblable for the admin and employee itself


def update_employee_name(session , employee , f_name , l_name):
    f_name = f_name.upper()
    l_name = l_name.upper()
    employee.f_name = f_name
    employee.l_name = l_name
    session.flush()

def update_employee_active(session , employee ,value):
    employee.active = value
    session.flush()

def update_employee_photo(session,employee,value):
    employee.photo = value
    session.flush()

def update_employee_social(session,employee,value):
    employee.socialMedia = value
    session.flush()