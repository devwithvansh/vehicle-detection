from sqlalchemy import or_
from sqlalchemy.orm import Session
import re

from app.models.vehicle import Vehicle
from app.schemas.vehicle import VehicleCreate, VehicleUpdate

def normalize_vehicle_number(vehicle_number: str) -> str:
    """
    Normalizes vehicle numbers by removing spaces, dashes, and the broad arrow.
    Specifically handles Indian Army formats.
    """
    if not vehicle_number:
        return ""
    # Remove broad arrow and other symbols
    clean = re.sub(r"[^A-Z0-9]", "", vehicle_number.upper())
    return clean

def get_vehicle_by_number(db: Session, vehicle_number: str) -> Vehicle | None:
    normalized = normalize_vehicle_number(vehicle_number)
    if not normalized:
        return None
    return db.query(Vehicle).filter(Vehicle.vehicle_number == normalized).first()

def create_vehicle(db: Session, payload: VehicleCreate) -> Vehicle:
    data = payload.model_dump()
    data["vehicle_number"] = normalize_vehicle_number(data["vehicle_number"])
    
    # Check if already exists to prevent duplicates if not handled by caller
    existing = get_vehicle_by_number(db, data["vehicle_number"])
    if existing:
        return update_vehicle(db, existing, VehicleUpdate(**data))
        
    vehicle = Vehicle(**data)
    db.add(vehicle)
    db.commit()
    db.refresh(vehicle)
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
        like = f"%{query}%"
        q = q.filter(
            or_(
                Vehicle.vehicle_number.ilike(like),
                Vehicle.driver_name.ilike(like),
                Vehicle.unit_name.ilike(like),
                Vehicle.vehicle_type.ilike(like),
            )
        )
    return q.order_by(Vehicle.created_at.desc()).offset(skip).limit(limit).all()
