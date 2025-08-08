
import smtplib
from email.message import EmailMessage

def send_email_console(to_email: str, subject: str, body: str, host="localhost", port=1025):
    # For local dev, use: python -m smtpd -c DebuggingServer -n localhost:1025
    msg = EmailMessage()
    msg["From"] = "noreply@brickbot.local"
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)
    try:
        with smtplib.SMTP(host, port) as s:
            s.send_message(msg)
        return True
    except Exception as e:
        print("[EMAIL DEBUG]", subject, "->", to_email)
        print(body)
        print("[EMAIL ERROR]", e)
        return False

def send_whatsapp_stub(number: str, message: str):
    # TODO: Integrate Twilio/Meta WhatsApp Business
    print(f"[WHATSAPP STUB] to {number}: {message}")
    return True
