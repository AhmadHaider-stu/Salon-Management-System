from sqlalchemy import Integer , Float, Column, ForeignKey , DateTime , Enum, String,Text,Boolean
from sqlalchemy.orm import relationship
from app.database import Base 
from app.enums.enum import AppointmentStatus



class Appointment(Base):
    __tablename__ = 'appointments'

    id = Column(Integer , primary_key = True)

    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    # add client phone number 
    phone = Column(String , nullable= False)
    total_price = Column(Float,nullable = False , default = 0)
    start_time = Column(DateTime , nullable = False)
    end_time = Column(DateTime)
    status = Column(Enum(AppointmentStatus) , nullable = False , default = AppointmentStatus.PENDING)
    note = Column(Text) # change it to text 
    confirmation_sent = Column(Boolean, nullable=False, default=False)

    # Define Many - to - Many relationships 

    client = relationship('Client', back_populates = 'appointments')
    appointment_services = relationship('AppointmentService', back_populates = "appointments")