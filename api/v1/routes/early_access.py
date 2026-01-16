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

def send_early_access_email(form_data: EarlyAccessForm):
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
        subject = f"New Early Access Request: {form_data.name} - {form_data.organization}"
        
        current_time = datetime.now().strftime("%B %d, %Y at %I:%M %p UTC")
        
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
        <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; color: #1f2937; background-color: #f3f4f6; margin: 0; padding: 0;">
            <div style="max-width: 600px; margin: 40px auto; background-color: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);">
                
                <!-- Header -->
                <div style="background-color: #1f2937; padding: 32px 40px; text-align: center;">
                    <h1 style="margin: 0; color: #ffffff; font-size: 24px; font-weight: 700; letter-spacing: -0.025em;">Ree-fond</h1>
                    <p style="margin: 8px 0 0 0; color: #9ca3af; font-size: 14px;">Infrastructure Pilot Program</p>
                </div>

                <!-- Main Content -->
                <div style="padding: 40px;">
                    <div style="margin-bottom: 24px;">
                        <span style="background-color: #d1fae5; color: #065f46; padding: 4px 12px; border-radius: 16px; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;">New Registration</span>
                        <h2 style="margin: 16px 0 8px 0; font-size: 20px; color: #111827;">Early Access Applicant</h2>
                        <p style="margin: 0; color: #6b7280; font-size: 14px;">Received on {current_time}</p>
                    </div>

                    <div style="background-color: #f9fafb; border-radius: 8px; border: 1px solid #e5e7eb; padding: 24px;">
                        
                        <!-- Contact Info Grid -->
                        <table style="width: 100%; border-collapse: collapse;">
                            <tr>
                                <td style="padding-bottom: 16px; width: 50%; vertical-align: top;">
                                    <h4 style="margin: 0 0 4px 0; color: #374151; font-size: 11px; text-transform: uppercase; letter-spacing: 0.05em;">Full Name</h4>
                                    <p style="margin: 0; color: #111827; font-weight: 500;">{form_data.name}</p>
                                </td>
                                <td style="padding-bottom: 16px; width: 50%; vertical-align: top;">
                                    <h4 style="margin: 0 0 4px 0; color: #374151; font-size: 11px; text-transform: uppercase; letter-spacing: 0.05em;">Organization</h4>
                                    <p style="margin: 0; color: #111827; font-weight: 500;">{form_data.organization}</p>
                                </td>
                            </tr>
                            <tr>
                                <td style="padding-bottom: 16px; width: 50%; vertical-align: top;">
                                    <h4 style="margin: 0 0 4px 0; color: #374151; font-size: 11px; text-transform: uppercase; letter-spacing: 0.05em;">Email Address</h4>
                                    <a href="mailto:{form_data.email}" style="margin: 0; color: #2563eb; text-decoration: none; font-weight: 500;">{form_data.email}</a>
                                </td>
                                <td style="padding-bottom: 16px; width: 50%; vertical-align: top;">
                                    <h4 style="margin: 0 0 4px 0; color: #374151; font-size: 11px; text-transform: uppercase; letter-spacing: 0.05em;">Phone Number</h4>
                                    <p style="margin: 0; color: #111827; font-weight: 500;">{form_data.phone}</p>
                                </td>
                            </tr>
                            <tr>
                                <td colspan="2" style="vertical-align: top;">
                                    <h4 style="margin: 0 0 4px 0; color: #374151; font-size: 11px; text-transform: uppercase; letter-spacing: 0.05em;">User Type</h4>
                                    <div style="display: inline-block; background-color: #e0f2fe; color: #0369a1; padding: 4px 10px; border-radius: 4px; font-size: 13px; font-weight: 600;">
                                        {form_data.type.replace('_', ' ').title()}
                                    </div>
                                </td>
                            </tr>
                        </table>

                        {pain_point_section}
                    </div>

                    <div style="margin-top: 32px; text-align: center;">
                        <a href="mailto:{form_data.email}" style="display: inline-block; background-color: #1f2937; color: #ffffff; padding: 12px 24px; border-radius: 6px; text-decoration: none; font-weight: 500; font-size: 14px;">Reply to Applicant</a>
                    </div>
                </div>

                <!-- Footer -->
                <div style="background-color: #f3f4f6; padding: 24px 40px; text-align: center; border-top: 1px solid #e5e7eb;">
                    <p style="margin: 0; color: #6b7280; font-size: 12px;">© {datetime.now().year} Ree-fond Systems. All rights reserved.</p>
                    <p style="margin: 8px 0 0 0; color: #9ca3af; font-size: 11px;">This is an automated notification from the early access portal.</p>
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
        © {datetime.now().year} Ree-fond Systems
        """
        
        # Create sendSmtpEmail instance
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=[{"email": receiver_email, "name": "Command Center"}],
            sender={"email": sender_email, "name": "Ree-fond Pilot Operations"},
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
    background_tasks.add_task(send_early_access_email, form)
    
    return {
        "message": "You're on the list. We will contact you when Phase 1 pilots begin.",
        "status": "success"
    }
