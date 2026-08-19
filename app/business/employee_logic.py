from app.CRUD.employee import *
from app.exceptions.employee import *
from app.CRUD.employee_service import add_employee_service  , del_service_by_employee
from app.services.cloudinary_client import upload_photo as cloudinary_upload
from app.services.phone_validation import is_valid_phone, format_phone

# HELPER
def get_or_raise(session, employeeID):
    employee = get_employee(session=session, employeeID=employeeID)
    if employee[0] == 'FAIL':
        raise NotFoundEmployee()
    return employee[1]

# def update_social(session, employeeID, newSocial):
#     try:
#         employee = get_or_raise(session=session, employeeID=employeeID)
#         update_employee_social(session=session, employee=employee[1], value=newSocial)
#         session.commit()
#     except:
#         session.rollback()
#         raise

# def update_photo(session, employeeID, newPhoto):
#     try:
#         employee = get_or_raise(session=session, employeeID=employeeID)
#         update_employee_photo(session=session, employee=employee[1], value=newPhoto)
#         session.commit()
#     except:
#         session.rollback()
#         raise

# def activate_employee(session, employeeID):
#     try:
#         employee = get_or_raise(session=session, employeeID=employeeID)
#         update_employee_active(session=session, employee=employee[1], value=True)
#         session.commit()
#     except:
#         session.rollback()
#         raise

# def deactivate_employee(session, employeeID):
#     try:
#         employee = get_or_raise(session=session, employeeID=employeeID)
#         update_employee_active(session=session, employee=employee[1], value=False)
#         session.commit()
#     except:
#         session.rollback()
#         raise

def update_employee_photo_upload(session, employeeID, file):
    try:
        status, employee = get_employee(session=session, employeeID=employeeID)
        if status == 'FAIL':
            raise NotFoundEmployee()
        photo_url = cloudinary_upload(file.file, folder="employee_photos")
        update_employee_photo(session=session, employee=employee, value=photo_url)
        session.commit()
        return photo_url
    except:
        session.rollback()
        raise


def alter_employee(session, employeeID, data):
    try:
        employee = get_or_raise(session=session, employeeID=employeeID)
        updates = data.model_dump(exclude_unset=True)

        if 'phone' in updates:
            if not is_valid_phone(updates['phone'], "AE"):
                raise InvalidPhoneNumber()
            updates['phone'] = format_phone(updates['phone'], "AE")

        for field, value in updates.items():
            if field in ('f_name', 'l_name'):
                value = value.upper()
            setattr(employee, field, value)
        session.commit()
        session.refresh(employee)
        return employee
    except:
        session.rollback()
        raise

def assign_employee_services(session , employeeID , servicesID):
    try:
        get_or_raise(session=session,employeeID=employeeID)
        del_service_by_employee(session=session , employeeID=employeeID)        
        add_employee_service(session=session , employeeID=employeeID , servicesID=servicesID)
        session.commit()
    except:
        session.rollback()
        raise