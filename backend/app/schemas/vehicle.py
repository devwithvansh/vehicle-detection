from datetime import datetime

from pydantic import BaseModel, Field


class VehicleBase(BaseModel):
    vehicle_number: str = Field(..., examples=["ARMY-22-C-1089"])
    driver_name: str
    unit_name: str
    vehicle_type: str
    purpose: str
    remarks: str | None = None
    operator_name: str


class VehicleCreate(VehicleBase):
    pass


class VehicleUpdate(BaseModel):
    driver_name: str | None = None
    unit_name: str | None = None
    vehicle_type: str | None = None
    purpose: str | None = None
    remarks: str | None = None
    operator_name: str | None = None


class VehicleRead(VehicleBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
