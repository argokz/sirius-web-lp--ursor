import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import List

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.auth import get_current_superuser
from app.database import get_db
from app.models.cms import MenuItem, PageBlock, PageView, SiteSetting
from app.models.content import ContentItem
from app.models.demo import DemoRequest, RequestStatus
from app.models.page import Page
from app.models.revision import PageRevision
from app.models.seo import SEOMetadata
from app.models.user import User
from app.schemas.auth import UserAdminCreate, UserAdminResponse, UserAdminUpdate, UserCreate
from app.schemas.cms import (
    MenuItemCreate,
    MenuItemResponse,
    MenuItemUpdate,
    PageBlockCreate,
    PageBlockResponse,
    PageBlockUpdate,
    PageCreate,
    PageResponse,
    PageUpdate,
    SiteSettingResponse,
    SiteSettingUpsert,
)
from app.schemas.content import ContentItemCreate, ContentItemResponse, ContentItemUpdate
from app.schemas.demo import DemoRequestResponse, DemoRequestStatusUpdate
from app.schemas.seo import SEOMetadataResponse, SEOMetadataUpdate
from app.services.auth import create_user as create_user_service

router = APIRouter()


def normalize_slug(slug: str) -> str:
    clean_slug = slug.strip().strip("/")
    if not clean_slug:
        raise HTTPException(status_code=400, detail="Slug is required")
    return clean_slug


def validate_payload_json(payload: str | None) -> str:
    if payload in (None, ""):
        return "{}"
    try:
        json.loads(payload)
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=400, detail=f"Payload must be valid JSON: {exc.msg}")
    return payload


@router.get("/content", response_model=List[ContentItemResponse])
def get_content_items(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_superuser),
):
    return db.query(ContentItem).offset(skip).limit(limit).all()


@router.post("/content", response_model=ContentItemResponse)
def create_content_item(
    item: ContentItemCreate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_superuser),
):
    db_item = ContentItem(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@router.put("/content/{item_id}", response_model=ContentItemResponse)
def update_content_item(
    item_id: int,
    item: ContentItemUpdate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_superuser),
):
    db_item = db.query(ContentItem).filter(ContentItem.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Content item not found")

    for field, value in item.dict(exclude_unset=True).items():
        setattr(db_item, field, value)

    db.commit()
    db.refresh(db_item)
    return db_item


@router.delete("/content/{item_id}")
def delete_content_item(
    item_id: int,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_superuser),
):
    db_item = db.query(ContentItem).filter(ContentItem.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Content item not found")

    db.delete(db_item)
    db.commit()
    return {"message": "Content item deleted"}


@router.get("/demo-requests", response_model=List[DemoRequestResponse])
def get_demo_requests(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_superuser),
):
    return (
        db.query(DemoRequest)
        .order_by(DemoRequest.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


@router.put("/demo-requests/{request_id}", response_model=DemoRequestResponse)
def update_demo_request_status(
    request_id: int,
    payload: DemoRequestStatusUpdate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_superuser),
):
    db_request = db.query(DemoRequest).filter(DemoRequest.id == request_id).first()
    if not db_request:
        raise HTTPException(status_code=404, detail="Demo request not found")

    db_request.status = payload.status
    db.commit()
    db.refresh(db_request)
    return db_request


# SVG не принимаем: /uploads раздаётся с того же адреса, что и сайт, и скрипт в SVG выполнился бы на itwin.kz.
UPLOAD_EXTENSIONS = {"png", "jpg", "jpeg", "webp", "gif", "pdf", "doc", "docx", "xls", "xlsx"}
UPLOAD_MAX_BYTES = 25 * 1024 * 1024
UPLOAD_CHUNK_BYTES = 1024 * 1024


@router.post("/upload")
def upload_file(
    file: UploadFile = File(...),
    admin_user: User = Depends(get_current_superuser),
):
    # Обычный def: запись файла синхронная, FastAPI выполнит её в пуле потоков, не блокируя цикл событий.
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)

    original_name = Path(file.filename or "").name
    if not original_name:
        raise HTTPException(status_code=400, detail="Filename is required")

    extension = Path(original_name).suffix.lower().lstrip(".")
    if extension not in UPLOAD_EXTENSIONS:
        raise HTTPException(status_code=400, detail="File type is not allowed")

    # Имя на диске — без исходного имени: в нём бывают пробелы, юникод и управляющие символы.
    safe_filename = f"{uuid.uuid4().hex}.{extension}"
    file_path = os.path.join(upload_dir, safe_filename)
    written = 0
    try:
        with open(file_path, "wb") as buffer:
            while chunk := file.file.read(UPLOAD_CHUNK_BYTES):
                written += len(chunk)
                if written > UPLOAD_MAX_BYTES:
                    raise HTTPException(status_code=413, detail="File is too large (max 25 MB)")
                buffer.write(chunk)
    except BaseException:
        Path(file_path).unlink(missing_ok=True)
        raise

    return {"filename": safe_filename, "path": file_path}


@router.get("/media")
def list_media(
    admin_user: User = Depends(get_current_superuser),
):
    """List all uploaded files in the uploads directory."""
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)

    image_exts = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".svg"}
    files = []

    for filename in os.listdir(upload_dir):
        filepath = os.path.join(upload_dir, filename)
        if not os.path.isfile(filepath):
            continue
        stat = os.stat(filepath)
        ext = Path(filename).suffix.lower()
        files.append({
            "filename": filename,
            "path": f"uploads/{filename}",
            "url": f"/uploads/{filename}",
            "size": stat.st_size,
            "modified": stat.st_mtime,
            "is_image": ext in image_exts,
            "ext": ext.lstrip(".")
        })

    return sorted(files, key=lambda x: x["modified"], reverse=True)


@router.delete("/media/{filename}")
def delete_media(
    filename: str,
    admin_user: User = Depends(get_current_superuser),
):
    """Delete a file from the uploads directory."""
    safe_name = Path(filename).name
    if safe_name != filename:
        raise HTTPException(status_code=400, detail="Invalid filename")

    filepath = os.path.join("uploads", safe_name)
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="File not found")

    os.remove(filepath)
    return {"message": "Файл удалён"}


@router.get("/analytics")
def get_analytics(
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_superuser),
):
    today_start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    status_counts = db.query(DemoRequest.status, func.count(DemoRequest.id)).group_by(DemoRequest.status).all()
    top_pages = (
        db.query(PageView.path, func.count(PageView.id).label("views"))
        .group_by(PageView.path)
        .order_by(func.count(PageView.id).desc())
        .limit(8)
        .all()
    )
    recent_demo_requests = (
        db.query(DemoRequest)
        .order_by(DemoRequest.created_at.desc())
        .limit(5)
        .all()
    )

    return {
        "total_demo_requests": db.query(DemoRequest).count(),
        "pending_requests": db.query(DemoRequest).filter(DemoRequest.status == RequestStatus.PENDING).count(),
        "total_content_items": db.query(ContentItem).count(),
        "total_pages": db.query(Page).count(),
        "active_pages": db.query(Page).filter(Page.is_active.is_(True)).count(),
        "total_blocks": db.query(PageBlock).count(),
        "active_blocks": db.query(PageBlock).filter(PageBlock.is_active.is_(True)).count(),
        "menu_items": db.query(MenuItem).count(),
        "active_menu_items": db.query(MenuItem).filter(MenuItem.is_active.is_(True)).count(),
        "page_views": db.query(PageView).count(),
        "views_today": db.query(PageView).filter(PageView.created_at >= today_start).count(),
        "requests_by_status": [
            {"status": status_value.value if hasattr(status_value, "value") else str(status_value), "count": count}
            for status_value, count in status_counts
        ],
        "top_pages": [{"path": path, "views": views} for path, views in top_pages],
        "recent_demo_requests": [
            {
                "id": request.id,
                "full_name": request.full_name,
                "email": request.email,
                "company": request.company,
                "status": request.status.value if hasattr(request.status, "value") else str(request.status),
                "created_at": request.created_at.isoformat() if request.created_at else None,
            }
            for request in recent_demo_requests
        ],
    }


@router.get("/users", response_model=List[UserAdminResponse])
def get_users(
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_superuser),
):
    return db.query(User).order_by(User.created_at.desc()).all()


@router.post("/users", response_model=UserAdminResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    payload: UserAdminCreate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_superuser),
):
    if len(payload.password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters long")

    existing_user = db.query(User).filter(User.email == payload.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user_data = UserCreate(
        email=payload.email,
        password=payload.password,
        full_name=payload.full_name,
    )
    return create_user_service(
        db=db,
        user=user_data,
        is_superuser=payload.is_superuser,
        is_active=payload.is_active,
    )


@router.put("/users/{user_id}", response_model=UserAdminResponse)
def update_user(
    user_id: int,
    payload: UserAdminUpdate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_superuser),
):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if user_id == admin_user.id and payload.is_superuser is False:
        raise HTTPException(status_code=400, detail="You cannot remove your own superuser role")

    for field, value in payload.dict(exclude_unset=True).items():
        setattr(db_user, field, value)

    db.commit()
    db.refresh(db_user)
    return db_user


@router.get("/pages", response_model=List[PageResponse])
def get_pages(
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_superuser),
):
    return db.query(Page).order_by(Page.title.asc()).all()


@router.post("/pages", response_model=PageResponse, status_code=status.HTTP_201_CREATED)
def create_page(
    payload: PageCreate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_superuser),
):
    slug = normalize_slug(payload.slug)
    if db.query(Page).filter(Page.slug == slug).first():
        raise HTTPException(status_code=400, detail="Page slug already exists")

    page = Page(slug=slug, title=payload.title, is_active=payload.is_active)
    db.add(page)
    db.commit()
    db.refresh(page)
    return page


@router.put("/pages/{page_id}", response_model=PageResponse)
def update_page(
    page_id: int,
    payload: PageUpdate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_superuser),
):
    page = db.query(Page).filter(Page.id == page_id).first()
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")

    update_data = payload.dict(exclude_unset=True)
    if "slug" in update_data and update_data["slug"] is not None:
        slug = normalize_slug(update_data["slug"])
        duplicate = db.query(Page).filter(Page.slug == slug, Page.id != page_id).first()
        if duplicate:
            raise HTTPException(status_code=400, detail="Page slug already exists")
        page.slug = slug
        update_data.pop("slug")

    for field, value in update_data.items():
        setattr(page, field, value)

    db.commit()
    db.refresh(page)
    return page


@router.delete("/pages/{page_id}")
def delete_page(
    page_id: int,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_superuser),
):
    page = db.query(Page).filter(Page.id == page_id).first()
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")

    db.query(PageBlock).filter(PageBlock.page_id == page_id).delete()
    db.query(MenuItem).filter(MenuItem.page_id == page_id).update({MenuItem.page_id: None})
    db.query(ContentItem).filter(ContentItem.page_id == page_id).delete()
    db.query(SEOMetadata).filter(SEOMetadata.page_id == page_id).delete()
    # ревизии публикаций: без этого backref обнуляет page_id (NOT NULL) и удаление падает с 500
    db.query(PageRevision).filter(PageRevision.page_id == page_id).delete()
    db.delete(page)
    db.commit()
    return {"message": "Page deleted"}

@router.post("/pages/{page_id}/publish")
def publish_page(
    page_id: int,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_superuser),
):
    page = db.query(Page).filter(Page.id == page_id).first()
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")

    blocks = (
        db.query(PageBlock)
        .filter(PageBlock.page_id == page_id, PageBlock.is_active.is_(True))
        .order_by(PageBlock.sort_order.asc(), PageBlock.id.asc())
        .all()
    )
    
    blocks_list = []
    for block in blocks:
        blocks_list.append({
            "id": block.id,
            "page_id": block.page_id,
            "block_key": block.block_key,
            "block_type": block.block_type,
            "eyebrow": block.eyebrow,
            "title": block.title,
            "body": block.body,
            "payload": block.payload,
            "sort_order": block.sort_order,
            "is_active": block.is_active,
            "created_at": block.created_at.isoformat() if block.created_at else None,
            "updated_at": block.updated_at.isoformat() if block.updated_at else None,
        })
    
    revision = PageRevision(
        page_id=page_id,
        blocks_payload=json.dumps(blocks_list, ensure_ascii=False)
    )
    db.add(revision)
    db.commit()
    
    return {"message": "Страница опубликована", "revision_id": revision.id}


@router.get("/pages/{page_id}/blocks", response_model=List[PageBlockResponse])
def get_page_blocks(
    page_id: int,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_superuser),
):
    page = db.query(Page).filter(Page.id == page_id).first()
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")

    return (
        db.query(PageBlock)
        .filter(PageBlock.page_id == page_id)
        .order_by(PageBlock.sort_order.asc(), PageBlock.id.asc())
        .all()
    )


@router.post("/pages/{page_id}/blocks", response_model=PageBlockResponse, status_code=status.HTTP_201_CREATED)
def create_page_block(
    page_id: int,
    payload: PageBlockCreate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_superuser),
):
    page = db.query(Page).filter(Page.id == page_id).first()
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")

    block_data = payload.dict()
    block_data["payload"] = validate_payload_json(block_data.get("payload"))
    block = PageBlock(page_id=page_id, **block_data)
    db.add(block)
    db.commit()
    db.refresh(block)
    return block


@router.put("/blocks/{block_id}", response_model=PageBlockResponse)
def update_page_block(
    block_id: int,
    payload: PageBlockUpdate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_superuser),
):
    block = db.query(PageBlock).filter(PageBlock.id == block_id).first()
    if not block:
        raise HTTPException(status_code=404, detail="Block not found")

    update_data = payload.dict(exclude_unset=True)
    if "payload" in update_data:
        update_data["payload"] = validate_payload_json(update_data.get("payload"))

    for field, value in update_data.items():
        setattr(block, field, value)

    db.commit()
    db.refresh(block)
    return block


@router.delete("/blocks/{block_id}")
def delete_page_block(
    block_id: int,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_superuser),
):
    block = db.query(PageBlock).filter(PageBlock.id == block_id).first()
    if not block:
        raise HTTPException(status_code=404, detail="Block not found")

    db.delete(block)
    db.commit()
    return {"message": "Block deleted"}


@router.get("/menu-items", response_model=List[MenuItemResponse])
def get_menu_items(
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_superuser),
):
    return db.query(MenuItem).order_by(MenuItem.sort_order.asc(), MenuItem.id.asc()).all()


@router.post("/menu-items", response_model=MenuItemResponse, status_code=status.HTTP_201_CREATED)
def create_menu_item(
    payload: MenuItemCreate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_superuser),
):
    item = MenuItem(**payload.dict())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.put("/menu-items/{item_id}", response_model=MenuItemResponse)
def update_menu_item(
    item_id: int,
    payload: MenuItemUpdate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_superuser),
):
    item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")

    for field, value in payload.dict(exclude_unset=True).items():
        setattr(item, field, value)

    db.commit()
    db.refresh(item)
    return item


@router.delete("/menu-items/{item_id}")
def delete_menu_item(
    item_id: int,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_superuser),
):
    item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")

    db.delete(item)
    db.commit()
    return {"message": "Menu item deleted"}


@router.get("/settings", response_model=List[SiteSettingResponse])
def get_settings(
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_superuser),
):
    return db.query(SiteSetting).order_by(SiteSetting.group_name.asc(), SiteSetting.id.asc()).all()


@router.put("/settings", response_model=List[SiteSettingResponse])
def upsert_settings(
    payload: List[SiteSettingUpsert],
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_superuser),
):
    for item in payload:
        setting = db.query(SiteSetting).filter(SiteSetting.key == item.key).first()
        if not setting:
            setting = SiteSetting(key=item.key)
            db.add(setting)

        setting.value = item.value
        setting.label = item.label
        setting.group_name = item.group_name
        setting.field_type = item.field_type

    db.commit()
    return db.query(SiteSetting).order_by(SiteSetting.group_name.asc(), SiteSetting.id.asc()).all()


@router.delete("/settings/{setting_key}")
def delete_setting(
    setting_key: str,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_superuser),
):
    setting = db.query(SiteSetting).filter(SiteSetting.key == setting_key).first()
    if not setting:
        raise HTTPException(status_code=404, detail="Setting not found")

    db.delete(setting)
    db.commit()
    return {"message": "Setting deleted"}


@router.get("/seo", response_model=SEOMetadataResponse)
def get_seo_metadata(
    page_slug: str = Query(default="home"),
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_superuser),
):
    page = db.query(Page).filter(Page.slug == page_slug).first()
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")

    metadata = db.query(SEOMetadata).filter(SEOMetadata.page_id == page.id).first()
    if not metadata:
        return SEOMetadataResponse(page_id=page.id)
    return metadata


@router.put("/seo", response_model=SEOMetadataResponse)
def upsert_seo_metadata(
    payload: SEOMetadataUpdate,
    page_slug: str = Query(default="home"),
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_superuser),
):
    page = db.query(Page).filter(Page.slug == page_slug).first()
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")

    metadata = db.query(SEOMetadata).filter(SEOMetadata.page_id == page.id).first()
    if not metadata:
        metadata = SEOMetadata(page_id=page.id)
        db.add(metadata)

    for field, value in payload.dict(exclude_unset=True).items():
        setattr(metadata, field, value)

    db.commit()
    db.refresh(metadata)
    return metadata
