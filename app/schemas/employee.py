from pydantic import BaseModel ,Field
from typing import Optional

class EmployeeResponse(BaseModel):
    id: int
    f_name: Optional[str] = Field(default=None, min_length=5, max_length=30)
    l_name: Optional[str] = Field(default=None, min_length=5, max_length=30)
    active: Optional[bool] = Field(default=1)
    photo: Optional[str] = Field(default=None)
    phone: Optional[str]
    bio: Optional[str] = Field(default=None)
    socialMedia: Optional[str] = Field(default=None)

class EmployeeRequest(BaseModel):
    f_name :str
    l_name : str
    active : Optional[bool]
    photo : Optional[str]
    phone : str

class EmployeeServicesRequest(BaseModel):
    services : list[int] = None

class EmployeeUpdate(BaseModel):
    f_name : Optional[str] = Field(default=None,min_length=5 , max_length=30)
    l_name : Optional[str] = Field(default=None,min_length=5 , max_length=30)
    active : Optional[bool] = Field(default=1)
    phone : Optional[str] = None
    bio : Optional[str]=Field(default=None)
    socialMedia : Optional[str]=Field(default=None)

