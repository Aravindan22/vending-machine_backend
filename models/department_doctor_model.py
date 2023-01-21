from backend.database import Base
from sqlalchemy import Column, String

class DoctorDepartment(Base):
    __tablename__ = 'doctor_department'
    doctor = Column(String(100), primary_key = True)
    department = Column(String(100), nullable=False)
    