from pydantic import BaseModel , Field 
from datetime import datetime
from app.enums.enum import AppointmentStatus
from typing import Optional
class ServiceSelection(BaseModel):
    employee_id: int
    service_id: int

class AppointmentCreate(BaseModel):
    start_time: datetime
    services: list[ServiceSelection]
    note : Optional[str]= Field(max_length=500)


class RescheduleRequest(BaseModel):
    start_time: datetime

class AddServiceRequest(BaseModel):
    employee_id: int
    service_id: int

class PriceUpdateRequest(BaseModel):
    price: float

