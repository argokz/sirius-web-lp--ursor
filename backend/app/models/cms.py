from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.sql import func
from app.database import Base


class PageBlock(Base):
    __tablename__ = "page_blocks"

    id = Column(Integer, primary_key=True, index=True)
    page_id = Column(Integer, ForeignKey("pages.id"), nullable=False, index=True)
    block_key = Column(String, nullable=False, index=True)
    block_type = Column(String, nullable=False, default="text")
    eyebrow = Column(String, nullable=True)
    title = Column(String, nullable=True)
    body = Column(Text, nullable=True)
    payload = Column(Text, nullable=True, default="{}")
    sort_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class MenuItem(Base):
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    url = Column(String, nullable=False)
    page_id = Column(Integer, ForeignKey("pages.id"), nullable=True)
    icon = Column(String, nullable=True)
    sort_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    is_external = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class SiteSetting(Base):
    __tablename__ = "site_settings"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, nullable=False, index=True)
    value = Column(Text, nullable=True)
    label = Column(String, nullable=True)
    group_name = Column(String, default="general", index=True)
    field_type = Column(String, default="text")
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class PageView(Base):
    __tablename__ = "page_views"

    id = Column(Integer, primary_key=True, index=True)
    path = Column(String, nullable=False, index=True)
    title = Column(String, nullable=True)
    referrer = Column(String, nullable=True)
    user_agent = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
