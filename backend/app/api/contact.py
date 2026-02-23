from fastapi import APIRouter
from pydantic import BaseModel, EmailStr
from typing import Optional

router = APIRouter()

class ContactMessage(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    message: str

@router.post("/contact")
async def send_contact_message(
    message: ContactMessage
):
    # Here you would integrate with email service (e.g., SendGrid, SMTP)
    # For now, just log and return success
    print(f"Contact message from {message.email}: {message.message}")
    
    # TODO: Send email notification
    # TODO: Save to database if needed
    
    return {
        "message": "Contact message received",
        "status": "success"
    }

