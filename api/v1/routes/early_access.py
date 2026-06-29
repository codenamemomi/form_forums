# api/v1/routes/early_access.py
from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional
import os
from dotenv import load_dotenv
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
import logging
from datetime import datetime

# Set up logging
logger = logging.getLogger(__name__)

load_dotenv()

early_access_router = APIRouter()

class EarlyAccessForm(BaseModel):
    name: str
    email: EmailStr
    phone: str
    organization: str
    type: str # individual, business, professional, partner
    painPoint: Optional[str] = None

# Configure Brevo API
configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = os.getenv("BREVO_API_KEY")

def send_early_access_email(form_data: EarlyAccessForm, organization_label: str = "Ree-fond"):
    try:
        # Check if credentials are configured
        brevo_api_key = os.getenv("BREVO_API_KEY")
        sender_email = os.getenv("SENDER_EMAIL")
        receiver_email = os.getenv("RECEIVER_EMAIL")
        
        if not brevo_api_key or not sender_email or not receiver_email:
            logger.error("Brevo credentials are not properly configured")
            return

        # Create API instance
        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
        
        # Create email content with Professional/Corporate theme
        organization_name = organization_label or form_data.organization or "Ree-fond"
        subject = f"New {organization_name} Early Access Request: {form_data.name}"
        
        current_time = datetime.now().strftime("%B %d, %Y at %I:%M %p UTC")
        program_label = "Infrastructure Pilot Program" if organization_name.lower() == "ree-fond" else "Waitlist Program"
        
        pain_point_section = ""
        if form_data.painPoint:
            pain_point_section = f"""
            <div style="margin-top: 24px; padding-top: 24px; border-top: 1px solid #e5e7eb;">
                <h4 style="margin: 0 0 8px 0; color: #374151; font-size: 14px; text-transform: uppercase; letter-spacing: 0.05em;">Key Pain Point</h4>
                <p style="margin: 0; color: #4b5563; font-style: italic;">"{form_data.painPoint}"</p>
            </div>
            """
            
        pain_point_text = ""
        if form_data.painPoint:
            pain_point_text = f"Key Pain Point: {form_data.painPoint}"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>New Early Access Registration</title>
        </head>
        <body style="margin: 0; padding: 0; background: #f3f4f6; font-family: Inter, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color: #111827;">
            <div style="max-width: 640px; margin: 32px auto; background: #ffffff; border: 1px solid #e5e7eb; border-radius: 16px; overflow: hidden; box-shadow: 0 6px 18px rgba(15, 23, 42, 0.05);">
                <div style="background: #111827; padding: 28px 32px; text-align: center;">
                    <div style="display: inline-block; padding: 6px 12px; border: 1px solid #374151; background: #f9fafb; border-radius: 999px; font-size: 10px; letter-spacing: 0.18em; text-transform: uppercase; color: #374151; margin-bottom: 12px;">
                        New Submission
                    </div>
                    <h1 style="margin: 0; color: #ffffff; font-size: 28px; font-weight: 700; letter-spacing: -0.04em;">{organization_name}</h1>
                    <p style="margin: 8px 0 0; color: #d1d5db; font-size: 14px;">{program_label}</p>
                </div>

                <div style="padding: 32px 32px 24px;">
                    <div style="margin-bottom: 20px;">
                        <span style="display: inline-block; background: #f3f4f6; color: #374151; padding: 6px 12px; border-radius: 999px; font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.16em; border: 1px solid #e5e7eb;">
                            New Registration
                        </span>
                        <h2 style="margin: 12px 0 8px; font-size: 24px; line-height: 1.2; color: #111827;">Early Access Applicant</h2>
                        <p style="margin: 0; color: #6b7280; font-size: 13px;">Received on {current_time}</p>
                    </div>

                    <div style="background: #f9fafb; border: 1px solid #e5e7eb; border-radius: 12px; padding: 20px;">
                        <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="border-collapse: collapse;">
                            <tr>
                                <td width="50%" valign="top" style="padding: 0 10px 16px 0;">
                                    <div style="font-size: 10px; font-weight: 700; letter-spacing: 0.16em; text-transform: uppercase; color: #6b7280; margin-bottom: 6px;">Full Name</div>
                                    <div style="font-size: 15px; font-weight: 600; color: #111827;">{form_data.name}</div>
                                </td>
                                <td style="padding-bottom: 16px; width: 50%; vertical-align: top;">
                                    <h4 style="margin: 0 0 4px 0; color: #374151; font-size: 11px; text-transform: uppercase; letter-spacing: 0.05em;">Organization</h4>
                                    <p style="margin: 0; color: #111827; font-weight: 500;">{form_data.organization}</p>
                                </td>
                            </tr>
                            <tr>
                                <td width="50%" valign="top" style="padding: 0 10px 16px 0;">
                                    <div style="font-size: 10px; font-weight: 700; letter-spacing: 0.16em; text-transform: uppercase; color: #6b7280; margin-bottom: 6px;">Email Address</div>
                                    <a href="mailto:{form_data.email}" style="font-size: 15px; font-weight: 600; color: #1d4ed8; text-decoration: none;">{form_data.email}</a>
                                </td>
                                <td width="50%" valign="top" style="padding: 0 0 16px 10px;">
                                    <div style="font-size: 10px; font-weight: 700; letter-spacing: 0.16em; text-transform: uppercase; color: #6b7280; margin-bottom: 6px;">Phone Number</div>
                                    <div style="font-size: 15px; font-weight: 600; color: #111827;">{form_data.phone}</div>
                                </td>
                            </tr>
                            <tr>
                                <td colspan="2" valign="top" style="padding: 0;">
                                    <div style="font-size: 10px; font-weight: 700; letter-spacing: 0.16em; text-transform: uppercase; color: #6b7280; margin-bottom: 6px;">User Type</div>
                                    <div style="display: inline-block; background: #e5e7eb; color: #374151; padding: 6px 12px; border-radius: 999px; font-size: 12px; font-weight: 700;">
                                        {form_data.type.replace('_', ' ').title()}
                                    </div>
                                </td>
                            </tr>
                        </table>

                        {pain_point_section}
                    </div>

                    <div style="margin-top: 24px; text-align: center;">
                        <a href="mailto:{form_data.email}" style="display: inline-block; background: #111827; color: #ffffff; padding: 12px 22px; border-radius: 10px; text-decoration: none; font-weight: 600; font-size: 14px;">
                            Reply to Applicant
                        </a>
                    </div>
                </div>

                <div style="background: #f9fafb; padding: 20px 32px; text-align: center; border-top: 1px solid #e5e7eb;">
                    <p style="margin: 0; color: #6b7280; font-size: 12px;">© {datetime.now().year} {organization_name}. All rights reserved.</p>
                    <p style="margin: 8px 0 0; color: #9ca3b8; font-size: 11px;">This is an automated notification from the early access portal.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        text_content = f"""
        NEW EARLY ACCESS REGISTRATION
        ============================
        
        APPLICANT DETAILS
        ----------------
        Name: {form_data.name}
        Organization: {form_data.organization}
        Email: {form_data.email}
        Phone: {form_data.phone}
        Type: {form_data.type.replace('_', ' ').title()}
        
        {pain_point_text}
        
        Received on: {current_time}
        
        --------------------------------------------------
        © {datetime.now().year} {organization_name} Systems
        """
        
        # Create sendSmtpEmail instance
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=[{"email": receiver_email, "name": "Command Center"}],
            sender={"email": sender_email, "name": f"{organization_name} Pilot Operations"},
            subject=subject,
            html_content=html_content,
            text_content=text_content,
            reply_to={"email": form_data.email, "name": form_data.name}
        )
        
        # Send email
        api_response = api_instance.send_transac_email(send_smtp_email)
        logger.info(f"✅ Pilot registration email sent successfully. Message ID: {api_response.message_id}")
        
    except ApiException as e:
        logger.error(f"❌ Brevo API exception: {e}")
    except Exception as e:
        logger.error(f"❌ Unexpected error sending pilot registration: {e}")

@early_access_router.post("/early-access")
async def submit_early_access_form(form: EarlyAccessForm, background_tasks: BackgroundTasks):
    # Validate that Brevo credentials are configured
    brevo_api_key = os.getenv("BREVO_API_KEY")
    
    if not brevo_api_key:
        raise HTTPException(
            status_code=500,
            detail="Registration system is currently offline. Please try again later."
        )
    
    # Add background task to send email
    background_tasks.add_task(send_early_access_email, form, "Ree-fond")
    
    return {
        "message": "You're on the list. We will contact you when Phase 1 pilots begin.",
        "status": "success"
    }

@early_access_router.post("/ws-waitlist")
async def submit_ws_waitlist(form: EarlyAccessForm, background_tasks: BackgroundTasks):
    """Dedicated endpoint for the W's waitlist signup flow."""
    brevo_api_key = os.getenv("BREVO_API_KEY")

    if not brevo_api_key:
        raise HTTPException(
            status_code=500,
            detail="W's waitlist is currently unavailable. Please try again later."
        )

    background_tasks.add_task(send_early_access_email, form, "W")

    return {
        "message": "You've been added to the W's waitlist.",
        "status": "success"
    }
