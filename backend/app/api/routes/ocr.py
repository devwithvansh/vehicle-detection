from pathlib import Path

from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.orm import Session

from ai.image_utils import save_upload, storage_path
from ai.ocr_engine import run_ocr
from ai.preprocess import preprocess_plate_image
from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.image import CapturedImage
from app.models.log import MovementType
from app.models.user import User
from app.schemas.ocr import OCRResult
from app.services.log_service import create_vehicle_log, infer_next_movement
from app.services.vehicle_service import get_vehicle_by_number

router = APIRouter(prefix="/ocr", tags=["ocr"])


@router.get("/history")
def image_history(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    rows = (
        db.query(CapturedImage)
        .order_by(CapturedImage.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return [
        {
            "id": item.id,
            "detected_number": item.detected_number,
            "confidence_score": item.confidence_score,
            "original_path": item.original_path,
            "processed_path": item.processed_path,
            "camera_location_id": item.camera_location_id,
            "created_at": item.created_at,
        }
        for item in rows
    ]


@router.post("/capture", response_model=OCRResult)
async def capture_image(
    image: UploadFile = File(...),
    camera_location_id: int | None = Form(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    original_path = await save_upload(image, "captures")
    processed_path = storage_path("processed", f"{Path(original_path).stem}_processed.jpg")
    preprocess_plate_image(original_path, processed_path)
    detected_number, confidence = run_ocr(processed_path)
    captured = CapturedImage(
        original_path=original_path,
        processed_path=str(processed_path),
        detected_number=detected_number,
        confidence_score=confidence,
        camera_location_id=camera_location_id,
    )
    db.add(captured)
    db.commit()
    db.refresh(captured)

    vehicle = get_vehicle_by_number(db, detected_number) if detected_number else None
    if vehicle:
        movement = infer_next_movement(db, vehicle.id)
        create_vehicle_log(
            db,
            vehicle_id=vehicle.id,
            operator_id=current_user.id,
            movement_type=movement,
            camera_location_id=camera_location_id,
            captured_image_id=captured.id,
            confidence_score=confidence,
            audit_note="Auto logged from OCR capture",
        )
        message = f"Registered vehicle found. {movement.value} marked."
    else:
        message = "Vehicle not registered. Redirect to registration with detected number."

    return OCRResult(
        image_id=captured.id,
        detected_number=detected_number,
        confidence_score=confidence,
        vehicle_exists=vehicle is not None,
        vehicle_id=vehicle.id if vehicle else None,
        original_path=original_path,
        processed_path=str(processed_path),
        message=message,
    )
