import os
import uuid
from fastapi import UploadFile
from typing import List

UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


def save_image(file: UploadFile) -> str:
    ext = file.filename.split(".")[-1] if "." in file.filename else "jpg"
    filename = f"{uuid.uuid4()}.{ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    contents = file.file.read()

    if not contents:
        raise ValueError("Empty file")

    with open(file_path, "wb") as f:
        f.write(contents)

    return f"/uploads/{filename}"


def save_multiple_images(files: List[UploadFile]) -> List[str]:
    return [save_image(file) for file in files]