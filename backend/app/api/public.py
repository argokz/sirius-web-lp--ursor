from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.demo import DemoRequest
from app.models.page import Page
from app.models.content import ContentItem
from app.schemas.demo import DemoRequestCreate, DemoRequestResponse
from app.schemas.content import ContentItemResponse

router = APIRouter()

@router.post("/demo-requests", response_model=DemoRequestResponse)
def create_demo_request(
    request: DemoRequestCreate,
    db: Session = Depends(get_db)
):
    db_request = DemoRequest(**request.dict())
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request

@router.get("/pages/{slug}/content", response_model=List[ContentItemResponse])
def get_page_content(slug: str, db: Session = Depends(get_db)):
    page = db.query(Page).filter(Page.slug == slug).first()
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")
    
    content = db.query(ContentItem).filter(ContentItem.page_id == page.id).all()
    return content


