from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.log import VehicleLog
from app.models.user import User
from app.models.vehicle import Vehicle
from app.services.log_service import active_vehicle_count, daily_movements, suspicious_count

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary")
def dashboard_summary(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    today = date.today()
    vehicles_today = db.query(VehicleLog).filter(func.date(VehicleLog.created_at) == today).count()
    total_vehicles = db.query(Vehicle).count()
    recent = (
        db.query(VehicleLog)
        .options(joinedload(VehicleLog.vehicle), joinedload(VehicleLog.operator), joinedload(VehicleLog.camera))
        .order_by(VehicleLog.created_at.desc())
        .limit(8)
        .all()
    )
    return {
        "stats": {
            "vehicles_today": vehicles_today,
            "active_inside": active_vehicle_count(db),
            "total_registered": total_vehicles,
            "suspicious_entries": suspicious_count(db),
        },
        "daily_movement": daily_movements(db),
        "recent_activity": [
            {
                "id": item.id,
                "vehicle_number": item.vehicle.vehicle_number,
                "movement_type": item.movement_type.value,
                "operator": item.operator.full_name,
                "camera": item.camera.name if item.camera else "Unassigned",
                "created_at": item.created_at,
            }
            for item in recent
        ],
    }
