from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from app.database import Base


class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer , primary_key = True)

    f_name = Column(String , nullable = False)
    l_name = Column(String , nullable = False)
    email = Column(String , unique = True , index = True)
    phone = Column(String , nullable = False , unique = True , index = True)



    # Define Many - to - Many relationships 
    
    appointments = relationship('Appointment' , back_populates = 'client')

    # Define One - to - One relationships 

    user = relationship('User' , back_populates = 'client')



