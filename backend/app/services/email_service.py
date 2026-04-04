import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings


def _send_email(to_email: str, subject: str, html_body: str):
    """Send an email via SMTP (Gmail compatible)."""
    if not settings.SMTP_USER or not settings.SMTP_PASSWORD:
        print(f"[EMAIL SKIPPED] No SMTP credentials configured. Would send to {to_email}: {subject}")
        return

    msg = MIMEMultipart("alternative")
    msg["From"] = settings.SMTP_FROM_EMAIL or settings.SMTP_USER
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(html_body, "html"))

    try:
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.sendmail(msg["From"], to_email, msg.as_string())
        print(f"[EMAIL SENT] {subject} → {to_email}")
    except Exception as e:
        print(f"[EMAIL ERROR] Failed to send to {to_email}: {e}")


def send_approval_email(to_email: str, full_name: str | None):
    name = full_name or "Provider"
    subject = "KasaUP — Your Provider Account is Approved!"
    html = f"""
    <div style="font-family: 'Segoe UI', Arial, sans-serif; max-width: 520px; margin: 0 auto; background: #0e0c1a; border-radius: 16px; padding: 40px 32px; color: #e8e8f0;">
        <h1 style="margin: 0 0 8px; font-size: 28px; color: #fff;">
            Kasa<span style="color: #a78bfa;">up</span>
        </h1>
        <p style="color: rgba(255,255,255,0.4); font-size: 13px; margin: 0 0 32px;">Marketplace for Local Services</p>
        
        <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 12px; padding: 20px; margin-bottom: 24px;">
            <p style="margin: 0; font-size: 15px; color: #10b981; font-weight: 600;">✓ Account Approved</p>
        </div>
        
        <p style="color: #fff; font-size: 16px; margin: 0 0 12px;">Hi {name},</p>
        <p style="color: rgba(255,255,255,0.6); font-size: 14px; line-height: 1.7; margin: 0 0 24px;">
            Great news! Your provider account on <strong style="color: #a78bfa;">KasaUP</strong> has been reviewed and approved by our team. 
            You can now log in and start setting up your shop profile, adding services, and receiving bookings.
        </p>
        
        <p style="color: rgba(255,255,255,0.3); font-size: 12px; margin: 24px 0 0; text-align: center;">
            — The KasaUP Team
        </p>
    </div>
    """
    _send_email(to_email, subject, html)


def send_rejection_email(to_email: str, full_name: str | None):
    name = full_name or "Applicant"
    subject = "KasaUP — Provider Application Update"
    html = f"""
    <div style="font-family: 'Segoe UI', Arial, sans-serif; max-width: 520px; margin: 0 auto; background: #0e0c1a; border-radius: 16px; padding: 40px 32px; color: #e8e8f0;">
        <h1 style="margin: 0 0 8px; font-size: 28px; color: #fff;">
            Kasa<span style="color: #a78bfa;">up</span>
        </h1>
        <p style="color: rgba(255,255,255,0.4); font-size: 13px; margin: 0 0 32px;">Marketplace for Local Services</p>
        
        <div style="background: rgba(248, 113, 113, 0.1); border: 1px solid rgba(248, 113, 113, 0.3); border-radius: 12px; padding: 20px; margin-bottom: 24px;">
            <p style="margin: 0; font-size: 15px; color: #f87171; font-weight: 600;">Application Not Approved</p>
        </div>
        
        <p style="color: #fff; font-size: 16px; margin: 0 0 12px;">Hi {name},</p>
        <p style="color: rgba(255,255,255,0.6); font-size: 14px; line-height: 1.7; margin: 0 0 24px;">
            Thank you for your interest in becoming a provider on <strong style="color: #a78bfa;">KasaUP</strong>. 
            After reviewing your application, we were unable to approve your account at this time.
            Your account has been removed from our system. You are welcome to re-apply in the future.
        </p>
        
        <p style="color: rgba(255,255,255,0.3); font-size: 12px; margin: 24px 0 0; text-align: center;">
            — The KasaUP Team
        </p>
    </div>
    """
    _send_email(to_email, subject, html)
