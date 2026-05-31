from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.vehicle import Vehicle
from app.schemas.vehicle import VehicleCreate, VehicleUpdate


def normalize_vehicle_number(vehicle_number: str) -> str:
    return "".join(vehicle_number.upper().replace("-", " ").split())


def get_vehicle_by_number(db: Session, vehicle_number: str) -> Vehicle | None:
    normalized = normalize_vehicle_number(vehicle_number)
    return db.query(Vehicle).filter(Vehicle.vehicle_number == normalized).first()


def create_vehicle(db: Session, payload: VehicleCreate) -> Vehicle:
    data = payload.model_dump()
    data["vehicle_number"] = normalize_vehicle_number(data["vehicle_number"])
    vehicle = Vehicle(**data)
    db.add(vehicle)
    db.commit()
    db.refresh(vehicle)
    return vehicle


def update_vehicle(db: Session, vehicle: Vehicle, payload: VehicleUpdate) -> Vehicle:
    for key, value in payload.model_dump(exclude_unset=True).items():
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
