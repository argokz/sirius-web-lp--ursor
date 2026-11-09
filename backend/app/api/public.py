from typing import Dict, List

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.cms import MenuItem, PageBlock, PageView, SiteSetting
from app.models.content import ContentItem
from app.models.demo import DemoRequest
from app.models.page import Page
from app.models.revision import PageRevision
from app.models.seo import SEOMetadata
from app.rate_limit import rate_limit
from app.schemas.cms import MenuItemResponse, PageViewCreate, PublicPageResponse
from app.schemas.content import ContentItemResponse
from app.schemas.demo import DemoRequestCreate, DemoRequestResponse

router = APIRouter()


@router.post(
    "/demo-requests",
    response_model=DemoRequestResponse,
    dependencies=[Depends(rate_limit("forms", limit=5, window_seconds=600))],
)
def create_demo_request(
    request: DemoRequestCreate,
    db: Session = Depends(get_db),
):
    db_request = DemoRequest(**request.dict())
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request


@router.get("/navigation", response_model=List[MenuItemResponse])
def get_navigation(db: Session = Depends(get_db)):
    return (
        db.query(MenuItem)
        .filter(MenuItem.is_active.is_(True))
        .order_by(MenuItem.sort_order.asc(), MenuItem.id.asc())
        .all()
    )


@router.get("/site-settings", response_model=Dict[str, str])
def get_site_settings(db: Session = Depends(get_db)):
    settings = db.query(SiteSetting).all()
    return {setting.key: setting.value or "" for setting in settings}


@router.get("/site/pages/{slug:path}", response_model=PublicPageResponse)
def get_site_page(slug: str, db: Session = Depends(get_db)):
    clean_slug = slug.strip().strip("/")
    page = db.query(Page).filter(Page.slug == clean_slug, Page.is_active.is_(True)).first()
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")

    revision = db.query(PageRevision).filter(PageRevision.page_id == page.id).order_by(PageRevision.created_at.desc()).first()
    
    if revision:
        import json
        blocks = json.loads(revision.blocks_payload)
    else:
        blocks = (
            db.query(PageBlock)
            .filter(PageBlock.page_id == page.id, PageBlock.is_active.is_(True))
            .order_by(PageBlock.sort_order.asc(), PageBlock.id.asc())
            .all()
        )
    seo = db.query(SEOMetadata).filter(SEOMetadata.page_id == page.id).first()
    return {"page": page, "blocks": blocks, "seo": seo}


@router.post("/analytics/page-view")
def track_page_view(
    payload: PageViewCreate,
    request: Request,
    db: Session = Depends(get_db),
):
    path = payload.path.strip()[:500]
    if not path:
        return {"ok": False}

    page_view = PageView(
        path=path,
        title=(payload.title or "")[:300],
        referrer=(payload.referrer or request.headers.get("referer") or "")[:500],
        user_agent=(request.headers.get("user-agent") or "")[:1000],
    )
    db.add(page_view)
    db.commit()
    return {"ok": True}


@router.get("/pages/{slug}/content", response_model=List[ContentItemResponse])
def get_page_content(slug: str, db: Session = Depends(get_db)):
    page = db.query(Page).filter(Page.slug == slug).first()
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")

    return db.query(ContentItem).filter(ContentItem.page_id == page.id).all()


@router.post("/site/form-submit", dependencies=[Depends(rate_limit("forms", limit=5, window_seconds=600))])
async def submit_block_form(
    payload: dict,
    db: Session = Depends(get_db),
):
    """Handle form submissions from CMS form blocks."""
    name = str(payload.get("name", "")).strip()[:200]
    email = str(payload.get("email", "")).strip()[:200]
    message = str(payload.get("message", "")).strip()[:2000]
    page_slug = str(payload.get("page_slug", "")).strip()[:200]

    if not name or not email:
        raise HTTPException(status_code=422, detail="Имя и Email обязательны")
    if "@" not in email:
        raise HTTPException(status_code=422, detail="Проверьте адрес email")

    request = DemoRequest(
        full_name=name,
        email=email,
        message=f"[Форма со страницы /{page_slug}]\n{message}",
    )
    db.add(request)
    db.commit()
    return {"message": "Сообщение отправлено"}
