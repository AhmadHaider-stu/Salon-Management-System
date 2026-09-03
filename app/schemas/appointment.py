from pydantic import BaseModel , Field 
from datetime import datetime 
from datetime import date as date_type
from app.enums.enum import AppointmentStatus
from typing import Optional
from zoneinfo import ZoneInfo
now = datetime.now(ZoneInfo("Asia/Amman"))
class ServiceSelection(BaseModel):
    employee_id: int
    service_id: int

class AppointmentCreate(BaseModel):
    start_time: datetime
    services: list[ServiceSelection]
    note : Optional[str]= Field(default=None,max_length=500)


class RescheduleRequest(BaseModel):
    start_time: datetime

class AddServiceRequest(BaseModel):
    employee_id: int
    service_id: int

class PriceUpdateRequest(BaseModel):
    price: float

class AvailabilityRequest(BaseModel):
    services: list[ServiceSelection]
    date: date_type
    exclude_appointment_id: Optional[int] = None