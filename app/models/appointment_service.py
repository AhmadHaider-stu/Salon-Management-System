from sqlalchemy import Integer, Float, Column, ForeignKey , DateTime ,Enum  ,UniqueConstraint , Boolean
from sqlalchemy.orm import relationship
from app.database import Base 
from app.enums.enum import AppointmentStatus



class AppointmentService(Base):
    __tablename__ = 'appointment_services'
    id = Column(Integer , primary_key= True)

    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime)
    price = Column(Float, nullable=False)
    status = Column(Enum(AppointmentStatus) , default = AppointmentStatus.PENDING, nullable = False)
    reminder = Column(Boolean, nullable=False, default=False)
    appointment_id = Column(Integer, ForeignKey("appointments.id"), nullable=False)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    

    __table_args__ = (
        UniqueConstraint("employee_id", "service_id" , "appointment_id"),
    )


    # Define Many - to - Many relationships 
    
    employees = relationship('Employee', back_populates = 'appointment_services')
    services = relationship('Service', back_populates = 'appointment_services')
    appointments = relationship('Appointment', back_populates = 'appointment_services')