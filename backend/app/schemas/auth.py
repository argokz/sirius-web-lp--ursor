from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    is_active: bool
    is_superuser: bool

    class Config:
        from_attributes = True


class UserAdminCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    is_active: bool = True
    is_superuser: bool = False


class UserAdminUpdate(BaseModel):
    full_name: Optional[str] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None


class UserAdminResponse(UserResponse):
    created_at: Optional[datetime] = None

