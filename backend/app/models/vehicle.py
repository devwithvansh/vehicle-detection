from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class Vehicle(Base):
    __tablename__ = "vehicles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    vehicle_number: Mapped[str] = mapped_column(String(32), unique=True, index=True, nullable=False)
    driver_name: Mapped[str] = mapped_column(String(120), nullable=False)
    unit_name: Mapped[str] = mapped_column(String(120), nullable=False)
    vehicle_type: Mapped[str] = mapped_column(String(80), nullable=False)
    purpose: Mapped[str] = mapped_column(String(160), nullable=False)
    remarks: Mapped[str | None] = mapped_column(Text)
    operator_name: Mapped[str] = mapped_column(String(120), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    logs = relationship("VehicleLog", back_populates="vehicle")
