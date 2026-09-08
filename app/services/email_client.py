import httpx
from app.config import BREVO_API_KEY, FROM_EMAIL, FROM_NAME

BREVO_API_URL = "https://api.brevo.com/v3/smtp/email"


def send_email(to_email, subject, body):
    try:
        response = httpx.post(
            BREVO_API_URL,
            headers={
                "accept": "application/json",
                "api-key": BREVO_API_KEY,
                "content-type": "application/json",
            },
            json={
                "sender": {"name": FROM_NAME, "email": FROM_EMAIL},
                "to": [{"email": to_email}],
                "subject": subject,
                "textContent": body,
            },
            timeout=10,
        )
        if response.status_code >= 400:
            print(f"EMAIL FAILED to {to_email}: {response.status_code} {response.text}")
    except Exception as e:
        print(f"EMAIL FAILED to {to_email}: {e}")