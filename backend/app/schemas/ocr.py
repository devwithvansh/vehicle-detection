from pydantic import BaseModel


class OCRResult(BaseModel):
    image_id: int
    detected_number: str | None
    confidence_score: float
    vehicle_exists: bool
    vehicle_id: int | None = None
    original_path: str
    processed_path: str | None = None
    message: str
