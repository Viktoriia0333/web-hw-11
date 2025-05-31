import cloudinary
import cloudinary.uploader
import os

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)


def upload_avatar(file, public_id: str):
    result = cloudinary.uploader.upload(file, public_id=public_id, folder="avatars")
    return result["secure_url"]
