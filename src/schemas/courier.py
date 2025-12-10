from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict

from db.models.couriers import CourierStatus, TransportType


class CourierBase(BaseModel):
    fullname: str
    phone: str
    transport_type: TransportType
    is_verified: bool = False
    is_available: bool = True
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class CourierCreateScheme(CourierBase):
    user_id: int


class CourierUpdateScheme(CourierBase):
    status: CourierStatus
    rating: Optional[float] = None
    completed_deliveries: Optional[int] = None


class CourierLocationUpdateScheme(BaseModel):
    lat: Optional[float] = None
    lon: Optional[float] = None


class CourierOutScheme(CourierBase):
    id: int
    user_id: int
    status: CourierStatus
    rating: float
    completed_deliveries: int

    model_config = ConfigDict(from_attributes=True)
