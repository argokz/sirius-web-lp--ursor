from sqlalchemy import Column, Integer, String, Text, DateTime, Enum as SQLEnum
from sqlalchemy.sql import func
import enum
from app.database import Base

class RequestStatus(str, enum.Enum):
    PENDING = "pending"
    CONTACTED = "contacted"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class DemoRequest(Base):
    __tablename__ = "demo_requests"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, nullable=False, index=True)
    phone = Column(String, nullable=True)
    company = Column(String, nullable=True)
    message = Column(Text, nullable=True)
    status = Column(SQLEnum(RequestStatus), default=RequestStatus.PENDING)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

