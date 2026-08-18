from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

class Employee(Base):
    __tablename__ = 'employees'
    id = Column(Integer, primary_key = True)

    f_name = Column(String, nullable = False)
    l_name = Column(String, nullable = False)
    email = Column(String , nullable = False , unique = True)
    photo = Column(String)
    socialMedia = Column(String)
    active = Column(Boolean, nullable = False)
    bio = Column(String)
    phone = Column(String , nullable = False , unique = True)
    # Define Many - to - Many relationships 

    appointment_services = relationship('AppointmentService',back_populates = 'employees')
    employee_services = relationship('EmployeeService', back_populates = 'employee')
    employee_schedule = relationship('EmployeeSchedule' , back_populates= 'employee' )
    
    # Define One - to - One relationships

    user = relationship('User' , back_populates = 'employee')
