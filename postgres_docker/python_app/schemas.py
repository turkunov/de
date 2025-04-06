from pydantic import BaseModel

class UserBase(BaseModel):
    id: str
    name: str
    surname: str
    gender: str
    img: str

class User(UserBase):
    pass