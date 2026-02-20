from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Page(Base):
    __tablename__ = "pages"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    content_items = relationship("ContentItem", back_populates="page")
    media_files = relationship("MediaFile", back_populates="page")
    sections = relationship("Section", back_populates="page")
    seo_metadata = relationship("SEOMetadata", back_populates="page", uselist=False)

class Section(Base):
    __tablename__ = "sections"

    id = Column(Integer, primary_key=True, index=True)
    page_id = Column(Integer, ForeignKey("pages.id"), nullable=False)
    section_key = Column(String, nullable=False, index=True)
    section_order = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    page = relationship("Page", back_populates="sections")
    content_items = relationship("ContentItem", back_populates="section")
    media_files = relationship("MediaFile", back_populates="section")

