import os 
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.environ.get('CLIENT_ID' , None)
CLIENT_SECRET = os.environ.get('CLIENT_SECRET' , None)
CLOUDINARY_CLOUD_NAME = os.environ.get('CLOUDINARY_CLOUD_NAME' , None)
CLOUDINARY_API_KEY = os.environ.get('CLOUDINARY_API_KEY' , None)
CLOUDINARY_API_SECRET = os.environ.get('CLOUDINARY_API_SECRET' , None)
GMAIL_USER = os.environ.get('GMAIL_USER' , None)
GMAIL_APP_PASSWORD = os.environ.get('GMAIL_APP_PASSWORD' , None)
FROM_EMAIL = os.environ.get('FROM_EMAIL' , None)
FROM_NAME = os.environ.get('FROM_NAME' , None)
BREVO_API_KEY = os.environ.get('BREVO_API_KEY' , None)