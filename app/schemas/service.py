from pydantic import BaseModel ,Field
from app.enums.enum import ServiceCategory
from typing import Optional


class ServiceCreate(BaseModel):
    category : ServiceCategory
    description : str = Field( max_length=30)
    price : float = Field(ge=10 ,le=500)
    time_duration : int = Field(ge=10,le=180)

class ServiceUpdate(BaseModel):
    category : Optional[ServiceCategory] = None
    description : Optional[str] = Field(default=None, max_length=30)
    price : Optional[float] = Field(default=None,ge=10 ,le=500)
    time_duration : Optional[int] = Field(default=None,ge=10,le=180)
    active : Optional[bool] = None

class ServiceResponse(BaseModel):
    id : int
    category : ServiceCategory
    description : str
    price : float 
    active : bool
    time_duration : int
    