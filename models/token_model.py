from ..database import Base
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime

class Token(Base):
    __tablename__ = 'token'
    id = Column(Integer, primary_key=True, autoincrement=True)
    doctor = Column(String(100), )
    department = Column(String(100), nullable=False)
    token = Column(String(12), nullable=False)
    created_time = Column(DateTime, default=datetime.now, nullable= False)
    diagonsed = Column(Integer, nullable=False, 
                       default=False)

    
    