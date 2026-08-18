from sqlalchemy import Column, Integer, String, Boolean, Float ,Enum
from sqlalchemy.orm import relationship
from app.database import Base
from app.enums.enum import ServiceCategory


class Service(Base):
    __tablename__ = 'services'

    id = Column(Integer , primary_key = True)

    category = Column(Enum(ServiceCategory), nullable = False)
    description = Column(String , nullable = False)
    price = Column(Float ,default = 0)
    active = Column(Boolean , default = True , nullable = False)
    time_duration = Column(Integer , default = 0 , nullable = False)
    
    
    # Define Many - to - Many relationships 
    appointment_services = relationship('AppointmentService', back_populates = "services")
    employee_services = relationship('EmployeeService', back_populates = 'services')

