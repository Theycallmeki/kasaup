import uuid
import boto3
from fastapi import UploadFile
from typing import List
from app.core.config import settings

s3 = boto3.client(
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

    s3.upload_fileobj(
        file.file,
        BUCKET,
        filename,
        ExtraArgs={"ContentType": file.content_type},
    )

    return f"https://{BUCKET}.s3.{settings.AWS_REGION}.amazonaws.com/{filename}"


def save_multiple_images(files: List[UploadFile]) -> List[str]:
    return [save_image(file) for file in files]