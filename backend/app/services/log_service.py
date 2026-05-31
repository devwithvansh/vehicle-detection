from datetime import datetime
from io import BytesIO, StringIO

from sqlalchemy import Date, cast, func
from sqlalchemy.orm import Session
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from app.models.log import MovementType, VehicleLog
from app.models.vehicle import Vehicle


def create_vehicle_log(
    db: Session,
    vehicle_id: int,
    operator_id: int,
    movement_type: MovementType,
    camera_location_id: int | None = None,
    captured_image_id: int | None = None,
    confidence_score: float | None = None,
    audit_note: str | None = None,
) -> VehicleLog:
    now = datetime.utcnow()
    log = VehicleLog(
        vehicle_id=vehicle_id,
        operator_id=operator_id,
        camera_location_id=camera_location_id,
        captured_image_id=captured_image_id,
        movement_type=movement_type,
        entry_time=now if movement_type == MovementType.entry else None,
        exit_time=now if movement_type == MovementType.exit else None,
        confidence_score=confidence_score,
        audit_note=audit_note,
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


def infer_next_movement(db: Session, vehicle_id: int) -> MovementType:
    latest = (
        db.query(VehicleLog)
        .filter(VehicleLog.vehicle_id == vehicle_id)
        .order_by(VehicleLog.created_at.desc())
        .first()
    )
    if latest and latest.movement_type == MovementType.entry:
        return MovementType.exit
    return MovementType.entry


def active_vehicle_count(db: Session) -> int:
    latest_subquery = (
        db.query(VehicleLog.vehicle_id, func.max(VehicleLog.created_at).label("latest"))
        .group_by(VehicleLog.vehicle_id)
        .subquery()
    )
    return (
        db.query(VehicleLog)
        .join(
            latest_subquery,
            (VehicleLog.vehicle_id == latest_subquery.c.vehicle_id)
            & (VehicleLog.created_at == latest_subquery.c.latest),
        )
        .filter(VehicleLog.movement_type == MovementType.entry)
        .count()
    )


def logs_to_csv(logs: list[VehicleLog]) -> str:
    output = StringIO()
    output.write("id,vehicle_number,movement_type,entry_time,exit_time,operator,camera,confidence\n")
    for log in logs:
        output.write(
            ",".join(
                [
                    str(log.id),
                    log.vehicle.vehicle_number,
                    log.movement_type.value,
                    str(log.entry_time or ""),
                    str(log.exit_time or ""),
                    log.operator.full_name,
                    log.camera.name if log.camera else "",
                    str(log.confidence_score or ""),
                ]
            )
            + "\n"
        )
    return output.getvalue()


def logs_to_pdf(logs: list[VehicleLog]) -> bytes:
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    y = height - 48
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(40, y, "Army Vehicle Movement Audit Log")
    y -= 28
    pdf.setFont("Helvetica", 8)
    for log in logs:
        if y < 48:
            pdf.showPage()
            pdf.setFont("Helvetica", 8)
            y = height - 48
        line = (
            f"#{log.id} | {log.vehicle.vehicle_number} | {log.movement_type.value} | "
            f"Entry: {log.entry_time or '-'} | Exit: {log.exit_time or '-'} | "
            f"Operator: {log.operator.full_name} | Camera: {log.camera.name if log.camera else '-'}"
        )
        pdf.drawString(40, y, line[:140])
        y -= 14
    pdf.save()
    buffer.seek(0)
    return buffer.read()


def daily_movements(db: Session, days: int = 7) -> list[dict[str, int | str]]:
    rows = (
        db.query(
            cast(VehicleLog.created_at, Date).label("day"),
            VehicleLog.movement_type,
            func.count(VehicleLog.id).label("total"),
        )
        .group_by("day", VehicleLog.movement_type)
        .order_by("day")
        .limit(days * 2)
        .all()
    )
    summary: dict[str, dict[str, int | str]] = {}
    for day, movement, total in rows:
        key = str(day)
        summary.setdefault(key, {"date": key, "entries": 0, "exits": 0})
        if movement == MovementType.entry:
            summary[key]["entries"] = int(total)
        else:
            summary[key]["exits"] = int(total)
    return list(summary.values())


def suspicious_count(db: Session) -> int:
    return (
        db.query(VehicleLog)
        .join(Vehicle)
        .filter((VehicleLog.confidence_score < 0.65) | Vehicle.remarks.ilike("%suspicious%"))
        .count()
    )
