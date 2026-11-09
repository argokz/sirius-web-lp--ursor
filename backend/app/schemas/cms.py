from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class PageCreate(BaseModel):
    slug: str
    title: str
    is_active: bool = True


class PageUpdate(BaseModel):
    slug: Optional[str] = None
    title: Optional[str] = None
    is_active: Optional[bool] = None


class PageResponse(BaseModel):
    id: int
    slug: str
    title: str
    is_active: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class PageBlockCreate(BaseModel):
    block_key: str
    block_type: str = "text"
    eyebrow: Optional[str] = None
    title: Optional[str] = None
    body: Optional[str] = None
    payload: Optional[str] = "{}"
    sort_order: int = 0
    is_active: bool = True


class PageBlockUpdate(BaseModel):
    block_key: Optional[str] = None
    block_type: Optional[str] = None
    eyebrow: Optional[str] = None
    title: Optional[str] = None
    body: Optional[str] = None
    payload: Optional[str] = None
    sort_order: Optional[int] = None
    is_active: Optional[bool] = None


class PageBlockResponse(BaseModel):
    id: int
    page_id: int
    block_key: str
    block_type: str
    eyebrow: Optional[str] = None
    title: Optional[str] = None
    body: Optional[str] = None
    payload: Optional[str] = "{}"
    sort_order: int
    is_active: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class MenuItemCreate(BaseModel):
    title: str
    url: str
    page_id: Optional[int] = None
    icon: Optional[str] = None
    sort_order: int = 0
    is_active: bool = True
    is_external: bool = False


class MenuItemUpdate(BaseModel):
    title: Optional[str] = None
    url: Optional[str] = None
    page_id: Optional[int] = None
    icon: Optional[str] = None
    sort_order: Optional[int] = None
    is_active: Optional[bool] = None
    is_external: Optional[bool] = None


class MenuItemResponse(BaseModel):
    id: int
    title: str
    url: str
    page_id: Optional[int] = None
    icon: Optional[str] = None
    sort_order: int
    is_active: bool
    is_external: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class SiteSettingUpsert(BaseModel):
    key: str
    value: Optional[str] = None
    label: Optional[str] = None
    group_name: str = "general"
    field_type: str = "text"


class SiteSettingResponse(BaseModel):
    id: int
    key: str
    value: Optional[str] = None
    label: Optional[str] = None
    group_name: str
    field_type: str
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class PageViewCreate(BaseModel):
    path: str
    title: Optional[str] = None
    referrer: Optional[str] = None


class PublicSeoResponse(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    keywords: Optional[str] = None
    og_title: Optional[str] = None
    og_description: Optional[str] = None
    og_image: Optional[str] = None
    og_type: str = "website"
    twitter_card: str = "summary_large_image"
    twitter_title: Optional[str] = None
    twitter_description: Optional[str] = None
    twitter_image: Optional[str] = None

    class Config:
        from_attributes = True


class PublicPageResponse(BaseModel):
    page: PageResponse
    blocks: List[PageBlockResponse]
    seo: Optional[PublicSeoResponse] = None
