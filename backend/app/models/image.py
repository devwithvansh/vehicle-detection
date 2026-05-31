from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class CapturedImage(Base):
    __tablename__ = "captured_images"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    original_path: Mapped[str] = mapped_column(String(500), nullable=False)
    processed_path: Mapped[str | None] = mapped_column(String(500))
    detected_number: Mapped[str | None] = mapped_column(String(32), index=True)
    confidence_score: Mapped[float | None] = mapped_column(Float)
    camera_location_id: Mapped[int | None] = mapped_column(ForeignKey("camera_locations.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    log = relationship("VehicleLog", back_populates="captured_image", uselist=False)
