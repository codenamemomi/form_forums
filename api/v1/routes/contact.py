from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, EmailStr
import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

load_dotenv()

contact_router = APIRouter()

class ContactForm(BaseModel):
    name: str
    email: EmailStr
    message: str

def send_email(form_data: ContactForm):
    sender_email = os.getenv("EMAIL_USERNAME")
    receiver_email = os.getenv("EMAIL_USERNAME")  
    email_password = os.getenv("EMAIL_PASSWORD")

    if not sender_email or not email_password:
        raise HTTPException(status_code=500, detail="Email credentials are not configured.")

    msg = EmailMessage()
    msg["Subject"] = "Connection From Portfolio"
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg.set_content(f"Name: {form_data.name}\nEmail: {form_data.email}\nMessage: {form_data.message}")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, email_password)
            server.send_message(msg)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")

@contact_router.post("/contact")
async def submit_contact_form(form: ContactForm, background_tasks: BackgroundTasks):
    background_tasks.add_task(send_email, form)
    return {"message": "Your message has been sent!"}
