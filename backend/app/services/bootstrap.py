from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.security import get_password_hash
from app.models.camera import CameraLocation
from app.models.user import User, UserRole


def seed_defaults(db: Session) -> None:
    settings = get_settings()
    admin = db.query(User).filter(User.username == settings.default_admin_username).first()
    if not admin:
        db.add(
            User(
                username=settings.default_admin_username,
                full_name="System Administrator",
                hashed_password=get_password_hash(settings.default_admin_password),
                role=UserRole.admin,
            )
        )
    if not db.query(CameraLocation).first():
        db.add_all(
            [
                CameraLocation(name="Main Gate", description="Primary entry checkpoint"),
                CameraLocation(name="Service Gate", description="Logistics and support movement"),
            ]
        )
    db.commit()
