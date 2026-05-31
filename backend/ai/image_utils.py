from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from app.core.config import get_settings


def storage_path(*parts: str) -> Path:
    root = Path(get_settings().storage_dir).resolve()
    path = root.joinpath(*parts)
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


async def save_upload(file: UploadFile, folder: str = "captures") -> str:
    suffix = Path(file.filename or "capture.jpg").suffix or ".jpg"
    target = storage_path(folder, f"{uuid4().hex}{suffix}")
    content = await file.read()
    target.write_bytes(content)
    return str(target)
