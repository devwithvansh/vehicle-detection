from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.orm import Session, joinedload

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.log import MovementType, VehicleLog
from app.models.user import User
from app.schemas.log import LogCreate, LogRead
from app.services.log_service import create_vehicle_log, logs_to_csv, logs_to_pdf

router = APIRouter(prefix="/logs", tags=["logs"])


def serialize_log(log: VehicleLog) -> LogRead:
    data = LogRead.model_validate(log)
    data.vehicle_number = log.vehicle.vehicle_number if log.vehicle else None
    data.operator_name = log.operator.full_name if log.operator else None
    data.camera_name = log.camera.name if log.camera else None
    return data


@router.get("", response_model=list[LogRead])
def list_logs(
    vehicle_number: str | None = None,
    movement_type: MovementType | None = None,
    skip: int = 0,
    limit: int = Query(25, le=200),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    query = db.query(VehicleLog).options(
        joinedload(VehicleLog.vehicle), joinedload(VehicleLog.operator), joinedload(VehicleLog.camera)
    )
    if vehicle_number:
        query = query.join(VehicleLog.vehicle).filter_by(vehicle_number=vehicle_number)
    if movement_type:
        query = query.filter(VehicleLog.movement_type == movement_type)
    logs = query.order_by(VehicleLog.created_at.desc()).offset(skip).limit(limit).all()
    return [serialize_log(log) for log in logs]


@router.post("", response_model=LogRead, status_code=201)
def create_log(
    payload: LogCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    log = create_vehicle_log(
        db,
        vehicle_id=payload.vehicle_id,
        operator_id=current_user.id,
        movement_type=MovementType(payload.movement_type),
        camera_location_id=payload.camera_location_id,
        captured_image_id=payload.captured_image_id,
        confidence_score=payload.confidence_score,
        audit_note=payload.audit_note,
    )
    return serialize_log(log)


@router.get("/export.csv")
def export_csv(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    logs = (
        db.query(VehicleLog)
        .options(joinedload(VehicleLog.vehicle), joinedload(VehicleLog.operator), joinedload(VehicleLog.camera))
        .order_by(VehicleLog.created_at.desc())
        .all()
    )
    return Response(
        logs_to_csv(logs),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=vehicle_logs.csv"},
    )


@router.get("/export.pdf")
def export_pdf(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    logs = (
        db.query(VehicleLog)
        .options(joinedload(VehicleLog.vehicle), joinedload(VehicleLog.operator), joinedload(VehicleLog.camera))
        .order_by(VehicleLog.created_at.desc())
        .all()
    )
    return Response(
        logs_to_pdf(logs),
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=vehicle_logs.pdf"},
    )
