from pydantic import BaseModel
from datetime import time
from app.enums.enum import DayOfWeek

class ScheduleEntry(BaseModel):
    day_of_week: DayOfWeek
    start_time: time
    end_time: time

class EmployeeScheduleUpdate(BaseModel):
    entries: list[ScheduleEntry]