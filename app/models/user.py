from sqlalchemy import Column, Integer, String, Enum , ForeignKey,Boolean 
from sqlalchemy.orm import relationship
from app.database import Base
from app.enums.enum import Role,Provider


class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key = True)

    f_name = Column(String, nullable = False)
    l_name = Column(String, nullable = False)
    email = Column(String , nullable = False , unique = True )
    oauth_sub = Column(String,unique=True , nullable=False)
    # oauth_providor = Column(Enum(Provider)) #nullable must be false but now for testing 
    role = Column(Enum(Role), nullable = False , default = Role.CLIENT)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    client_id = Column(Integer, ForeignKey("clients.id"))
    block = Column(Boolean , nullable=False , default=False)
    phone = Column(String , nullable = False , unique = True , index = True)


    # Define One - to - One relationships

    employee = relationship ('Employee' , back_populates = 'user')
    client = relationship('Client', back_populates = 'user')




