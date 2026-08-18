import smtplib
from email.mime.text import MIMEText
from app.config import GMAIL_USER, GMAIL_APP_PASSWORD, FROM_EMAIL , FROM_NAME


def send_email(to_email, subject, body):
    try:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = f"{FROM_NAME} <{FROM_EMAIL}>"
        msg['To'] = to_email

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            # server.starttls()
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            server.send_message(msg)
    except Exception as e:
        print(f"EMAIL FAILED to {to_email}: {e}")