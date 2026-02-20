from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from app.models.demo import RequestStatus

class DemoRequestCreate(BaseModel):
    full_name: str
    email: EmailStr
    phone: Optional[str] = None
    company: Optional[str] = None
    message: Optional[str] = None

class DemoRequestResponse(BaseModel):
    id: int
    full_name: str
    email: str
    phone: Optional[str]
    company: Optional[str]
    message: Optional[str]
    status: RequestStatus
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

