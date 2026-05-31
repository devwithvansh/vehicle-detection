from sqlalchemy import or_
from sqlalchemy.orm import Session
import re

from app.models.vehicle import Vehicle
from app.schemas.vehicle import VehicleCreate, VehicleUpdate
from app.models.log import MovementType

def normalize_vehicle_number(vehicle_number: str) -> str:
    """
    Normalizes vehicle numbers while PRESERVING the army arrow.
    """
    if not vehicle_number:
        return ""
    # Extract alphanumeric characters
    clean = re.sub(r"[^A-Z0-9]", "", vehicle_number.upper())
    # Always ensure it starts with the arrow for army vehicles
    return f"↑{clean}"

def get_vehicle_by_number(db: Session, vehicle_number: str) -> Vehicle | None:
    normalized = normalize_vehicle_number(vehicle_number)
    if not normalized:
        return None
    return db.query(Vehicle).filter(Vehicle.vehicle_number == normalized).first()

def create_vehicle(db: Session, payload: VehicleCreate, operator_id: int | None = None) -> Vehicle:
    data = payload.model_dump()
    data["vehicle_number"] = normalize_vehicle_number(data["vehicle_number"])
    
    existing = get_vehicle_by_number(db, data["vehicle_number"])
    if existing:
        return update_vehicle(db, existing, VehicleUpdate(**data))
        
    vehicle = Vehicle(**data)
    db.add(vehicle)
    db.commit()
    db.refresh(vehicle)
    
    # Automatically create an ENTRY log when a vehicle is first registered
    # Moved import inside to avoid circular dependency with log_service
    if operator_id:
        from app.services.log_service import create_vehicle_log
        create_vehicle_log(
            db,
            vehicle_id=vehicle.id,
            operator_id=operator_id,
            movement_type=MovementType.entry,
            audit_note="Initial entry log created upon registration"
        )
        
    return vehicle

def update_vehicle(db: Session, vehicle: Vehicle, payload: VehicleUpdate) -> Vehicle:
    for key, value in payload.model_dump(exclude_unset=True).items():
        if key == "vehicle_number":
            value = normalize_vehicle_number(value)
        setattr(vehicle, key, value)
    db.commit()
    db.refresh(vehicle)
    return vehicle

def search_vehicles(db: Session, query: str | None, skip: int, limit: int) -> list[Vehicle]:
    q = db.query(Vehicle)
    if query:
        # If searching, also normalize the query to match the stored format
        search_term = query.upper().replace("↑", "").strip()
        like = f"%{search_term}%"
        q = q.filter(
            or_(
                Vehicle.vehicle_number.ilike(f"%{search_term}%"),
                Vehicle.driver_name.ilike(like),
                Vehicle.unit_name.ilike(like),
                Vehicle.vehicle_type.ilike(like),
            )
        )
    return q.order_by(Vehicle.created_at.desc()).offset(skip).limit(limit).all()
