from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.demo import DemoRequest
from app.rate_limit import rate_limit

router = APIRouter()


class ContactMessage(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    email: EmailStr
    phone: Optional[str] = Field(default=None, max_length=50)
    message: str = Field(min_length=1, max_length=4000)


@router.post("/contact", dependencies=[Depends(rate_limit("forms", limit=5, window_seconds=600))])
def send_contact_message(message: ContactMessage, db: Session = Depends(get_db)):
    # Сообщения с «Контактов» попадают в тот же список заявок админки, что и заявки на демо.
    db.add(
        DemoRequest(
            full_name=message.name.strip(),
            email=message.email,
            phone=(message.phone or "").strip() or None,
            message=f"[Сообщение со страницы «Контакты»]\n{message.message.strip()}",
        )
    )
    db.commit()
    return {"message": "Contact message received", "status": "success"}
