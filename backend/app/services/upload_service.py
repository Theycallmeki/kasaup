import os
import uuid
from fastapi import UploadFile
from typing import List

UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


def save_image(file: UploadFile) -> str:
    ext = file.filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    return file_path


def save_multiple_images(files: List[UploadFile]) -> List[str]:
    return [save_image(file) for file in files]