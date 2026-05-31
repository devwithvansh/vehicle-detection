from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, Enum as SqlEnum, Float, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class MovementType(str, Enum):
    entry = "ENTRY"
    exit = "EXIT"


class VehicleLog(Base):
    __tablename__ = "vehicle_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    vehicle_id: Mapped[int] = mapped_column(ForeignKey("vehicles.id"), nullable=False)
    operator_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    camera_location_id: Mapped[int | None] = mapped_column(ForeignKey("camera_locations.id"))
    captured_image_id: Mapped[int | None] = mapped_column(ForeignKey("captured_images.id"))
    movement_type: Mapped[MovementType] = mapped_column(SqlEnum(MovementType), nullable=False)
    entry_time: Mapped[datetime | None] = mapped_column(DateTime)
    exit_time: Mapped[datetime | None] = mapped_column(DateTime)
    confidence_score: Mapped[float | None] = mapped_column(Float)
    audit_note: Mapped[str | None] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    vehicle = relationship("Vehicle", back_populates="logs")
    operator = relationship("User", back_populates="logs")
    camera = relationship("CameraLocation", back_populates="logs")
    captured_image = relationship("CapturedImage", back_populates="log")
