from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ContentItemCreate(BaseModel):
    page_id: Optional[int] = None
    section_id: Optional[int] = None
    content_type: str
    content_key: str
    content_value: str
    language: str = "ru"

class ContentItemUpdate(BaseModel):
    content_value: Optional[str] = None
    content_type: Optional[str] = None

class ContentItemResponse(BaseModel):
    id: int
    page_id: Optional[int]
    section_id: Optional[int]
    content_type: str
    content_key: str
    content_value: str
    language: str
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

