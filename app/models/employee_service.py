from sqlalchemy import Integer, Column, ForeignKey ,UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base 


class EmployeeService(Base):
    __tablename__ = 'employee_services'

    id = Column(Integer, primary_key=True)

    employee_id = Column(Integer, ForeignKey("employees.id"))
    service_id = Column(Integer, ForeignKey("services.id"))

    # Define Many - to - Many relationships 

    employee = relationship('Employee', back_populates = 'employee_services')
    services = relationship('Service', back_populates = 'employee_services')
    __table_args__ = (
        UniqueConstraint("employee_id", "service_id"),
    )




   
