import cloudinary
import cloudinary.uploader
from app.config import CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET

cloudinary.config(
    cloud_name=CLOUDINARY_CLOUD_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET,
    secure=True
)

def upload_photo(file, folder="employee_photos"):
    result = cloudinary.uploader.upload(file, folder=folder)
    return result['secure_url']

def delete_photo(public_id):
    cloudinary.uploader.destroy(public_id)