from pydantic import BaseModel
from typing import Union

class Token(BaseModel):
    doctor:str
    department:str
    token:str
    diagonsed:bool
    class Config:
        orm_mode = True