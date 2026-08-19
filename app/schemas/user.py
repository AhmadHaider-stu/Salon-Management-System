from pydantic import BaseModel ,Field
from app.enums.enum import Role
from typing import Optional


class UserResponse(BaseModel):
    id: int
    f_name: str
    l_name: str
    role: Role
    email: Optional[str] = None
    phone: Optional[str] = None
    employee_id: Optional[int] = None
    client_id: Optional[int] = None

class RenameUserRequest(BaseModel):
    f_name : str = Field(min_length=2,max_length=30)
    l_name : str = Field(min_length=2,max_length=30)


class PhoneUpdateRequest(BaseModel):
    phone: str