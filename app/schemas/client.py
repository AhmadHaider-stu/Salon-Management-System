from pydantic import BaseModel
from app.schemas.appointment import ServiceSelection
from datetime import datetime
from zoneinfo import ZoneInfo
now = datetime.now(ZoneInfo("Asia/Amman"))


class WalkInClientCreate(BaseModel):
    f_name: str
    l_name: str
    phone: str
    email: str | None = None

class WalkInBookingCreate(BaseModel):
    client: WalkInClientCreate
    services: list[ServiceSelection]  # reuse from appointment schema
    start_time: datetime

class ClientEdit(BaseModel):
    f_name: str
    l_name: str
    phone: str|None = None