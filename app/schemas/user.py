from typing import Optional

from pydantic import BaseModel, Field, ConfigDict, EmailStr


class UserBase(BaseModel):
    email:EmailStr


class User(UserBase):
    password: str = Field(..., min_length=8)


class UserCreate(UserBase):
    fio: str = Field(..., min_length=1)
    password:str = Field(...,min_length=8)


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    fio: Optional[str] = Field(None, min_length=1)
    password: Optional[str] = Field(None, min_length=8)
    is_admin: Optional[bool] = None


class UserOut(UserBase):
    id:int
    is_admin:bool
    fio: str = Field(..., min_length=1)

    model_config = ConfigDict(from_attributes=True)