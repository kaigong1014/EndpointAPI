from pydantic import BaseModel
from datetime import date


class UserBase(BaseModel):
    customer_name : str
    contact_email : str
    customer_input_date : date
    customer_input_address : str
    content : str
    url : str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id : int
    pass

    class Config:
        orm_mode = True