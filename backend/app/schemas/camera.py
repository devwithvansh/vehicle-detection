from datetime import datetime

from pydantic import BaseModel


class CameraCreate(BaseModel):
    name: str
    stream_url: str | None = None
    description: str | None = None
    is_active: bool = True


class CameraRead(CameraCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
