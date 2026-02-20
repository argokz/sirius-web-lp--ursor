from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class ContentItem(Base):
    __tablename__ = "content_items"

    id = Column(Integer, primary_key=True, index=True)
    page_id = Column(Integer, ForeignKey("pages.id"), nullable=True)
    section_id = Column(Integer, ForeignKey("sections.id"), nullable=True)
    content_type = Column(String, nullable=False)  # 'text', 'heading', 'title'
    content_key = Column(String, nullable=False, index=True)  # Unique key for content
    content_value = Column(Text, nullable=False)
    language = Column(String, default='ru')
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    page = relationship("Page", back_populates="content_items")
    section = relationship("Section", back_populates="content_items")

class MediaFile(Base):
    __tablename__ = "media_files"

    id = Column(Integer, primary_key=True, index=True)
    page_id = Column(Integer, ForeignKey("pages.id"), nullable=True)
    section_id = Column(Integer, ForeignKey("sections.id"), nullable=True)
    file_type = Column(String, nullable=False)  # 'image', 'video'
    file_path = Column(String, nullable=False)
    file_name = Column(String, nullable=False)
    alt_text = Column(String, nullable=True)
    mime_type = Column(String, nullable=True)
    file_size = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    page = relationship("Page", back_populates="media_files")
    section = relationship("Section", back_populates="media_files")

