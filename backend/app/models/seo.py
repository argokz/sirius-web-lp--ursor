from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class SEOMetadata(Base):
    __tablename__ = "seo_metadata"

    id = Column(Integer, primary_key=True, index=True)
    page_id = Column(Integer, ForeignKey("pages.id"), unique=True, nullable=False)
    title = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    keywords = Column(String, nullable=True)
    og_title = Column(String, nullable=True)
    og_description = Column(Text, nullable=True)
    og_image = Column(String, nullable=True)
    og_type = Column(String, default="website")
    twitter_card = Column(String, default="summary_large_image")
    twitter_title = Column(String, nullable=True)
    twitter_description = Column(Text, nullable=True)
    twitter_image = Column(String, nullable=True)

    page = relationship("Page", back_populates="seo_metadata")

