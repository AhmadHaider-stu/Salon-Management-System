from sqlalchemy import Column, Integer, Time, ForeignKey , Enum , UniqueConstraint , Boolean
from sqlalchemy.orm import relationship
from app.database import Base
from app.enums.enum import DayOfWeek
from datetime import time



class EmployeeSchedule(Base):
    __tablename__ = 'employee_schedule'

    id = Column(Integer , primary_key= True)

    employee_id = Column(Integer ,ForeignKey('employees.id') ,nullable=False)
    day_of_week = Column(Enum(DayOfWeek) , nullable=False)
    start_time = Column(Time , nullable = False , default= time(10))
    end_time = Column(Time , nullable = False , default= time(20,30))

    
    __table_args__ = (
        UniqueConstraint("employee_id", "day_of_week"),
    )
    # Relationships 
    employee = relationship('Employee' , back_populates= 'employee_schedule')

 