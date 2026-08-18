from app.models.employee_schedule import *

# add a day with start and end time 

def add_schedule_entry (session , employee_id , day_of_week , start_time = None, end_time = None):

    #check if exist before done it 
    status , exists = get_schedule_for_day(session=session , employee_id=employee_id , day_of_week= day_of_week)
    if (status == 'OK'):
        return 'FAIL'
    new_day = EmployeeSchedule(employee_id = employee_id,
                                day_of_week = day_of_week,
                                start_time = start_time,
                                end_time = end_time)
    session.add(new_day)
    session.flush()
    return 'OK',new_day

def get_schedule_for_employee (session , employee_id):
    days = session.query(EmployeeSchedule).filter(EmployeeSchedule.employee_id == employee_id).all()
    return days

def get_schedule_for_day (session , employee_id , day_of_week):
    day = session.query(EmployeeSchedule).filter(EmployeeSchedule.employee_id == employee_id,
                                                 EmployeeSchedule.day_of_week == day_of_week).one_or_none()
    if (day is None):
        return 'FAIL',None
    return 'OK',day

def delete_schedule_for_day(session , employee_id , day_of_week):
    day = get_schedule_for_day(session=session,employee_id=employee_id,day_of_week=day_of_week)
    if (day[1] == None):
        return 'OK'
    session.delete(day[1])
    session.flush()
    return 'OK'

def delete_schedule_for_employee(session, employee_id):
    days = session.query(EmployeeSchedule).filter(EmployeeSchedule.employee_id == employee_id).all()
    for day in days:
        session.delete(day)
    session.flush()
    return 'OK'