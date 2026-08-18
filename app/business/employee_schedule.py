from app.CRUD.employee_schedule import *
from app.exceptions.employee_schedule import *


from app.CRUD.employee_schedule import *
from app.exceptions.employee_schedule import *  # add InvalidScheduleTime to this file

def set_employee_schedule(session, employee_id, schedule_list):
    try:
        for entry in schedule_list:
            if entry['end_time'] <= entry['start_time']:
                raise InvalidScheduleTime()

        delete_schedule_for_employee(session=session, employee_id=employee_id)

        for entry in schedule_list:
            add_schedule_entry(
                session=session,
                employee_id=employee_id,
                day_of_week=entry['day_of_week'],
                start_time=entry['start_time'],
                end_time=entry['end_time']
            )
        session.commit()
    except:
        session.rollback()
        raise