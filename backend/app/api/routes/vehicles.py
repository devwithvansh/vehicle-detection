from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.vehicle import VehicleCreate, VehicleRead, VehicleUpdate
from app.services.vehicle_service import create_vehicle, get_vehicle_by_number, search_vehicles, update_vehicle

router = APIRouter(prefix="/vehicles", tags=["vehicles"])


@router.get("", response_model=list[VehicleRead])
def list_vehicles(
    q: str | None = None,
    skip: int = 0,
    limit: int = Query(20, le=100),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    return search_vehicles(db, q, skip, limit)


@router.post("", response_model=VehicleRead, status_code=201)
def register_vehicle(
    payload: VehicleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if get_vehicle_by_number(db, payload.vehicle_number):
        raise HTTPException(status_code=409, detail="Vehicle already registered")
    return create_vehicle(db, payload, operator_id=current_user.id)


@router.get("/{vehicle_number}", response_model=VehicleRead)
def get_vehicle(
    vehicle_number: str,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    vehicle = get_vehicle_by_number(db, vehicle_number)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle


@router.patch("/{vehicle_number}", response_model=VehicleRead)
def patch_vehicle(
    vehicle_number: str,
    payload: VehicleUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    vehicle = get_vehicle_by_number(db, vehicle_number)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return update_vehicle(db, vehicle, payload)
