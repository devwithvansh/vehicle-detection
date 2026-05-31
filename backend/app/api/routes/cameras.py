from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_admin
from app.db.session import get_db
from app.models.camera import CameraLocation
from app.models.user import User
from app.schemas.camera import CameraCreate, CameraRead

router = APIRouter(prefix="/cameras", tags=["cameras"])


@router.get("", response_model=list[CameraRead])
def list_cameras(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(CameraLocation).order_by(CameraLocation.name).all()


@router.post("", response_model=CameraRead, status_code=201)
def create_camera(
    payload: CameraCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    camera = CameraLocation(**payload.model_dump())
    db.add(camera)
    db.commit()
    db.refresh(camera)
    return camera
