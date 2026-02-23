from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.api.auth import get_current_superuser
from app.models.user import User
from app.models.content import ContentItem
from app.models.demo import DemoRequest, RequestStatus
from app.models.seo import SEOMetadata
from app.models.page import Page
from app.services.auth import create_user as create_user_service
from app.schemas.content import ContentItemCreate, ContentItemUpdate, ContentItemResponse
from app.schemas.demo import DemoRequestResponse, DemoRequestStatusUpdate
from app.schemas.seo import SEOMetadataUpdate, SEOMetadataResponse
from app.schemas.auth import UserAdminCreate, UserAdminUpdate, UserAdminResponse, UserCreate
import os
import shutil
import uuid
from pathlib import Path

router = APIRouter()

@router.get("/content", response_model=List[ContentItemResponse])
def get_content_items(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_superuser)
):
    items = db.query(ContentItem).offset(skip).limit(limit).all()
    return items

@router.post("/content", response_model=ContentItemResponse)
def create_content_item(
    item: ContentItemCreate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_superuser)
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
    admin_user: User = Depends(get_current_superuser)
):
    db_item = db.query(ContentItem).filter(ContentItem.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Content item not found")
    
    update_data = item.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_item, field, value)
    
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete("/content/{item_id}")
def delete_content_item(
    item_id: int,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_superuser)
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
    admin_user: User = Depends(get_current_superuser)
):
    requests = db.query(DemoRequest).offset(skip).limit(limit).all()
    return requests

@router.put("/demo-requests/{request_id}", response_model=DemoRequestResponse)
def update_demo_request_status(
    request_id: int,
    payload: DemoRequestStatusUpdate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_superuser)
):
    db_request = db.query(DemoRequest).filter(DemoRequest.id == request_id).first()
    if not db_request:
        raise HTTPException(status_code=404, detail="Demo request not found")
    
    db_request.status = payload.status
    db.commit()
    db.refresh(db_request)
    return db_request

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    admin_user: User = Depends(get_current_superuser)
):
    allowed_extensions = {
        "png", "jpg", "jpeg", "webp", "svg", "gif", "pdf", "doc", "docx", "xls", "xlsx"
    }
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)

    original_name = Path(file.filename or "").name
    if not original_name:
        raise HTTPException(status_code=400, detail="Filename is required")

    extension = Path(original_name).suffix.lower().replace(".", "")
    if extension and extension not in allowed_extensions:
        raise HTTPException(status_code=400, detail="File type is not allowed")

    safe_filename = f"{uuid.uuid4().hex}_{original_name.replace(' ', '_')}"
    file_path = os.path.join(upload_dir, safe_filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return {"filename": safe_filename, "path": file_path}

@router.get("/analytics")
def get_analytics(
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_superuser)
):
    total_requests = db.query(DemoRequest).count()
    pending_requests = db.query(DemoRequest).filter(DemoRequest.status == RequestStatus.PENDING).count()
    total_content = db.query(ContentItem).count()
    
    return {
        "total_demo_requests": total_requests,
        "pending_requests": pending_requests,
        "total_content_items": total_content
    }


@router.get("/users", response_model=List[UserAdminResponse])
def get_users(
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_superuser)
):
    users = db.query(User).order_by(User.created_at.desc()).all()
    return users


@router.post("/users", response_model=UserAdminResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    payload: UserAdminCreate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_superuser)
):
    if len(payload.password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters long")

    existing_user = db.query(User).filter(User.email == payload.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user_data = UserCreate(
        email=payload.email,
        password=payload.password,
        full_name=payload.full_name
    )
    db_user = create_user_service(
        db=db,
        user=user_data,
        is_superuser=payload.is_superuser,
        is_active=payload.is_active
    )
    return db_user


@router.put("/users/{user_id}", response_model=UserAdminResponse)
def update_user(
    user_id: int,
    payload: UserAdminUpdate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_superuser)
):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if user_id == admin_user.id and payload.is_superuser is False:
        raise HTTPException(status_code=400, detail="You cannot remove your own superuser role")

    update_data = payload.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_user, field, value)

    db.commit()
    db.refresh(db_user)
    return db_user


@router.get("/pages")
def get_pages(
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_superuser)
):
    pages = db.query(Page).order_by(Page.title.asc()).all()
    return [
        {"id": page.id, "slug": page.slug, "title": page.title, "is_active": page.is_active}
        for page in pages
    ]


@router.get("/seo", response_model=SEOMetadataResponse)
def get_seo_metadata(
    page_slug: str = Query(default="home"),
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_superuser)
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
    admin_user: User = Depends(get_current_superuser)
):
    page = db.query(Page).filter(Page.slug == page_slug).first()
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")

    metadata = db.query(SEOMetadata).filter(SEOMetadata.page_id == page.id).first()
    if not metadata:
        metadata = SEOMetadata(page_id=page.id)
        db.add(metadata)

    update_data = payload.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(metadata, field, value)

    db.commit()
    db.refresh(metadata)
    return metadata

