from datetime import datetime

from pydantic import BaseModel


class LogCreate(BaseModel):
    vehicle_id: int
    camera_location_id: int | None = None
    captured_image_id: int | None = None
    movement_type: str
    confidence_score: float | None = None
    audit_note: str | None = None


class LogRead(BaseModel):
    id: int
    vehicle_id: int
    operator_id: int
    camera_location_id: int | None
    captured_image_id: int | None
    movement_type: str
    entry_time: datetime | None
    exit_time: datetime | None
    confidence_score: float | None
    audit_note: str | None
    created_at: datetime
    vehicle_number: str | None = None
    operator_name: str | None = None
    camera_name: str | None = None

    class Config:
        from_attributes = True
