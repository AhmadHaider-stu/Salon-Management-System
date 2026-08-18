from pydantic import BaseModel ,Field
from app.enums.enum import Role


class UserResponse(BaseModel):
    id:int
    f_name: str
    l_name : str
    role : Role

class RenameUserRequest(BaseModel):
    f_name : str = Field(min_length=2,max_length=30)
    l_name : str = Field(min_length=2,max_length=30)
