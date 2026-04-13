import uuid
import boto3
from fastapi import UploadFile
from typing import List
from app.core.config import settings

def get_s3_client():
    """Lazily initialize S3 client to prevent startup crashes."""
    return boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION,
    )

BUCKET = settings.AWS_S3_BUCKET


def save_image(file: UploadFile) -> str:
    ext = file.filename.split(".")[-1] if "." in file.filename else "jpg"
    filename = f"{uuid.uuid4()}.{ext}"

    contents = file.file.read()

    if not contents:
        raise ValueError("Empty file")

    file.file.seek(0)

    s3_client = get_s3_client()
    s3_client.upload_fileobj(
        file.file,
        BUCKET,
        filename,
        ExtraArgs={"ContentType": file.content_type},
    )

    return f"https://{BUCKET}.s3.{settings.AWS_REGION}.amazonaws.com/{filename}"


def save_multiple_images(files: List[UploadFile]) -> List[str]:
    return [save_image(file) for file in files]


def delete_image_from_s3(url: str):
    """Deletes an image from S3 given its full URL."""
    if not url:
        return
    
    try:
   
        parts = url.split("/")
        if len(parts) < 4:
            return
            
        filename = parts[-1]
        
        if not url.startswith(f"https://{BUCKET}.s3.{settings.AWS_REGION}.amazonaws.com/"):
            return

        s3_client = get_s3_client()
        s3_client.delete_object(Bucket=BUCKET, Key=filename)
        print(f"Successfully deleted {filename} from S3")
    except Exception as e:
        print(f"Failed to delete {url} from S3: {e}")