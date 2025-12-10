from __future__ import annotations

import enum

from sqlalchemy import Boolean, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import BaseModel


class TransportType(str, enum.Enum):
    foot = "foot"
    bike = "bike"
    car = "car"
    moto = "moto"


class CourierStatus(str, enum.Enum):
    active = "active"
    offline = "offline"
    busy = "busy"


class Courier(BaseModel):
    __tablename__ = "couriers"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), unique=True, nullable=False
    )
    fullname: Mapped[str] = mapped_column(String(120))
    phone: Mapped[str] = mapped_column(String(25))
    status: Mapped[CourierStatus] = mapped_column(
        Enum(CourierStatus), default=CourierStatus.active
    )
    transport_type: Mapped[TransportType] = mapped_column(
        Enum(TransportType, name="transport_type_enum"), nullable=False
    )
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)

    rating: Mapped[float] = mapped_column(Float, default=5.0)
    completed_deliveries: Mapped[int] = mapped_column(
        Integer, default=0, nullable=False
    )

    # realtime location
    latitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    longitude: Mapped[float | None] = mapped_column(Float, nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="couriers")  # type: ignore # noqa: F821
