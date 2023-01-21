from pydantic import BaseModel
from typing import Union, List

class DoctorDepartment(BaseModel):
    doctor:str
    department:str
    class Config:
        orm_mode = True

    