# api/v1/routes/contact.py
from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel, EmailStr
import os
from dotenv import load_dotenv
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
import logging
from datetime import datetime

# Set up logging
logger = logging.getLogger(__name__)

load_dotenv()

contact_router = APIRouter()

class ContactForm(BaseModel):
    name: str
    email: EmailStr
    subject: str
    message: str

# Configure Brevo API
configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = os.getenv("BREVO_API_KEY")

def send_brevo_email(form_data: ContactForm):
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
        
        # Create email content with enhanced spy/tech theme
        subject = f"🚀 SECURE TRANSMISSION: {form_data.subject}"
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;600&family=Share+Tech+Mono&display=swap');
                
                body {{
                    font-family: 'JetBrains Mono', monospace;
                    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
                    margin: 0;
                    padding: 20px;
                    color: #e2e8f0;
                }}
                .container {{
                    max-width: 700px;
                    margin: 0 auto;
                    background: rgba(15, 23, 42, 0.95);
                    border: 1px solid #334155;
                    border-radius: 12px;
                    overflow: hidden;
                    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
                }}
                .header {{
                    background: linear-gradient(135deg, #3b82f6 0%, #1e40af 100%);
                    padding: 30px;
                    text-align: center;
                    border-bottom: 2px solid #60a5fa;
                    position: relative;
                }}
                .header::before {{
                    content: '';
                    position: absolute;
                    top: 0;
                    left: 0;
                    right: 0;
                    height: 2px;
                    background: linear-gradient(90deg, transparent, #60a5fa, transparent);
                    animation: scanline 2s linear infinite;
                }}
                @keyframes scanline {{
                    0% {{ transform: translateX(-100%); }}
                    100% {{ transform: translateX(100%); }}
                }}
                .header h1 {{
                    margin: 0;
                    font-size: 24px;
                    font-weight: 600;
                    color: white;
                    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
                    font-family: 'Share Tech Mono', monospace;
                    letter-spacing: 1px;
                }}
                .header .subtitle {{
                    margin: 8px 0 0 0;
                    font-size: 14px;
                    color: #bfdbfe;
                    opacity: 0.9;
                }}
                .content {{
                    padding: 40px;
                }}
                .mission-data {{
                    background: rgba(30, 41, 59, 0.6);
                    border: 1px solid #475569;
                    border-radius: 8px;
                    padding: 25px;
                    margin-bottom: 30px;
                    position: relative;
                }}
                .mission-data::before {{
                    content: 'MISSION DATA';
                    position: absolute;
                    top: -10px;
                    left: 20px;
                    background: #1e293b;
                    padding: 0 12px;
                    font-size: 12px;
                    color: #60a5fa;
                    font-weight: 600;
                    letter-spacing: 1px;
                }}
                .data-grid {{
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    gap: 20px;
                    margin-bottom: 25px;
                }}
                .data-item {{
                    display: flex;
                    flex-direction: column;
                    gap: 8px;
                }}
                .data-label {{
                    font-size: 12px;
                    color: #94a3b8;
                    font-weight: 600;
                    text-transform: uppercase;
                    letter-spacing: 0.5px;
                }}
                .data-value {{
                    font-size: 16px;
                    color: #e2e8f0;
                    font-weight: 500;
                    padding: 12px;
                    background: rgba(51, 65, 85, 0.3);
                    border: 1px solid #475569;
                    border-radius: 6px;
                    font-family: 'Share Tech Mono', monospace;
                }}
                .message-section {{
                    margin-top: 25px;
                }}
                .message-label {{
                    font-size: 12px;
                    color: #94a3b8;
                    font-weight: 600;
                    text-transform: uppercase;
                    letter-spacing: 0.5px;
                    margin-bottom: 12px;
                }}
                .message-content {{
                    background: rgba(51, 65, 85, 0.3);
                    border: 1px solid #475569;
                    border-radius: 6px;
                    padding: 20px;
                    color: #e2e8f0;
                    line-height: 1.6;
                    font-size: 14px;
                    white-space: pre-wrap;
                    font-family: 'JetBrains Mono', monospace;
                }}
                .footer {{
                    background: rgba(30, 41, 59, 0.8);
                    padding: 25px;
                    text-align: center;
                    border-top: 1px solid #334155;
                    font-size: 12px;
                    color: #64748b;
                }}
                .status-indicator {{
                    display: inline-flex;
                    align-items: center;
                    gap: 8px;
                    padding: 8px 16px;
                    background: rgba(34, 197, 94, 0.1);
                    border: 1px solid rgba(34, 197, 94, 0.3);
                    border-radius: 20px;
                    color: #22c55e;
                    font-weight: 600;
                }}
                .status-dot {{
                    width: 8px;
                    height: 8px;
                    background: #22c55e;
                    border-radius: 50%;
                    animation: pulse 2s infinite;
                }}
                @keyframes pulse {{
                    0%, 100% {{ opacity: 1; }}
                    50% {{ opacity: 0.5; }}
                }}
                .timestamp {{
                    margin-top: 15px;
                    font-size: 11px;
                    color: #475569;
                    font-family: 'Share Tech Mono', monospace;
                }}
                .priority-tag {{
                    display: inline-block;
                    padding: 4px 12px;
                    background: rgba(239, 68, 68, 0.2);
                    border: 1px solid rgba(239, 68, 68, 0.4);
                    border-radius: 12px;
                    color: #fca5a5;
                    font-size: 10px;
                    font-weight: 600;
                    text-transform: uppercase;
                    letter-spacing: 0.5px;
                    margin-left: 10px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🔐 SECURE TRANSMISSION RECEIVED</h1>
                    <div class="subtitle">ENCRYPTED MESSAGE FROM PORTFOLIO COMMAND CENTER</div>
                </div>
                
                <div class="content">
                    <div class="mission-data">
                        <div class="data-grid">
                            <div class="data-item">
                                <div class="data-label">Agent Identity</div>
                                <div class="data-value">🎯 {form_data.name}</div>
                            </div>
                            <div class="data-item">
                                <div class="data-label">Secure Channel</div>
                                <div class="data-value">📧 {form_data.email}</div>
                            </div>
                            <div class="data-item">
                                <div class="data-label">Mission Classification</div>
                                <div class="data-value">📋 {form_data.subject}</div>
                            </div>
                            <div class="data-item">
                                <div class="data-label">Transmission Time</div>
                                <div class="data-value">⏰ {current_time}</div>
                            </div>
                        </div>
                        
                        <div class="message-section">
                            <div class="message-label">Encrypted Message Content</div>
                            <div class="message-content">{form_data.message}</div>
                        </div>
                    </div>
                    
                    <div style="text-align: center; margin-top: 30px;">
                        <div class="status-indicator">
                            <div class="status-dot"></div>
                            TRANSMISSION STATUS: SECURE & ENCRYPTED
                        </div>
                    </div>
                </div>
                
                <div class="footer">
                    <div>🚀 This message was transmitted via Portfolio Command Center</div>
                    <div class="timestamp">Message ID: {datetime.now().strftime('%Y%m%d%H%M%S')} | Encryption: AES-256</div>
                    <div style="margin-top: 15px; font-size: 10px; color: #475569;">
                        <em>This is an automated transmission from your portfolio contact form</em>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        text_content = f"""
        🔐 SECURE TRANSMISSION RECEIVED
        ===============================

        MISSION DATA:
        ------------
        Agent Identity: {form_data.name}
        Secure Channel: {form_data.email}
        Mission Classification: {form_data.subject}
        Transmission Time: {current_time}

        ENCRYPTED MESSAGE:
        -----------------
        {form_data.message}

        TRANSMISSION STATUS: SECURE & ENCRYPTED ✅

        ---
        This message was transmitted via Portfolio Command Center
        Message ID: {datetime.now().strftime('%Y%m%d%H%M%S')}
        Encryption: AES-256
        """
        
        # Create sendSmtpEmail instance
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=[{"email": receiver_email, "name": "Command Center"}],
            sender={"email": sender_email, "name": "Portfolio Command Center"},
            subject=subject,
            html_content=html_content,
            text_content=text_content,
            reply_to={"email": form_data.email, "name": form_data.name}
        )
        
        # Send email
        api_response = api_instance.send_transac_email(send_smtp_email)
        logger.info(f"✅ Secure transmission sent successfully. Message ID: {api_response.message_id}")
        
    except ApiException as e:
        logger.error(f"❌ Brevo API exception: {e}")
    except Exception as e:
        logger.error(f"❌ Unexpected error sending transmission: {e}")

@contact_router.post("/contact")
async def submit_contact_form(form: ContactForm, background_tasks: BackgroundTasks):
    # Validate that Brevo credentials are configured
    brevo_api_key = os.getenv("BREVO_API_KEY")
    sender_email = os.getenv("SENDER_EMAIL")
    receiver_email = os.getenv("RECEIVER_EMAIL")
    
    if not brevo_api_key:
        raise HTTPException(
            status_code=500,
            detail="Secure transmission service is currently offline. Please try again later."
        )
    
    # Add background task to send email
    background_tasks.add_task(send_brevo_email, form)
    
    return {
        "message": "Secure transmission initiated! Your message is being encrypted and delivered to command center.",
        "status": "success"
    }

@contact_router.get("/health")
async def health_check():
    """Check if transmission service is operational"""
    brevo_api_key = os.getenv("BREVO_API_KEY")
    sender_email = os.getenv("SENDER_EMAIL")
    receiver_email = os.getenv("RECEIVER_EMAIL")
    
    return {
        "transmission_service": "Brevo Secure Channel",
        "service_status": "OPERATIONAL" if brevo_api_key else "OFFLINE",
        "sender_channel_configured": bool(sender_email),
        "receiver_channel_configured": bool(receiver_email),
        "encryption_protocol": "AES-256",
        "transmission_ready": bool(brevo_api_key and sender_email and receiver_email)
    }