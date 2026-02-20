from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.api.auth import get_current_user
from app.models.user import User
from app.models.content import ContentItem, MediaFile
from app.models.demo import DemoRequest
from app.models.seo import SEOMetadata
from app.schemas.content import ContentItemCreate, ContentItemUpdate, ContentItemResponse
from app.schemas.demo import DemoRequestResponse
from app.schemas.seo import SEOMetadataCreate, SEOMetadataUpdate
import os
import shutil

router = APIRouter()

@router.get("/content", response_model=List[ContentItemResponse])
def get_content_items(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    items = db.query(ContentItem).offset(skip).limit(limit).all()
    return items

@router.post("/content", response_model=ContentItemResponse)
def create_content_item(
    item: ContentItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
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
    current_user: User = Depends(get_current_user)
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
    current_user: User = Depends(get_current_user)
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
    current_user: User = Depends(get_current_user)
):
    requests = db.query(DemoRequest).offset(skip).limit(limit).all()
    return requests

@router.put("/demo-requests/{request_id}", response_model=DemoRequestResponse)
def update_demo_request_status(
    request_id: int,
    status: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_request = db.query(DemoRequest).filter(DemoRequest.id == request_id).first()
    if not db_request:
        raise HTTPException(status_code=404, detail="Demo request not found")
    
    db_request.status = status
    db.commit()
    db.refresh(db_request)
    return db_request

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)
    
    file_path = os.path.join(upload_dir, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return {"filename": file.filename, "path": file_path}

@router.get("/analytics")
def get_analytics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    total_requests = db.query(DemoRequest).count()
    pending_requests = db.query(DemoRequest).filter(DemoRequest.status == "pending").count()
    total_content = db.query(ContentItem).count()
    
    return {
        "total_demo_requests": total_requests,
        "pending_requests": pending_requests,
        "total_content_items": total_content
    }

