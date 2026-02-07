from pydantic import BaseModel, Field, ConfigDict, EmailStr


class UserBase(BaseModel):
    email:EmailStr

class User(UserBase):
    password: str = Field(..., min_length=8)

class UserCreate(UserBase):
    fio: str = Field(..., min_length=1)
    password:str = Field(...,min_length=8)

class UserOut(UserBase):
    id:int
    is_admin:bool
    fio: str = Field(..., min_length=1)

    model_config = ConfigDict(from_attributes=True)