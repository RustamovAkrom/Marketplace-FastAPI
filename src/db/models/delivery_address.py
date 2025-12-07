from __future__ import annotations

from sqlalchemy import Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import BaseModel


class DeliveryAddress(BaseModel):
    __tablename__ = "delivery_addresses"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    country: Mapped[str] = mapped_column(String(64))
    city: Mapped[str] = mapped_column(String(64))
    street: Mapped[str] = mapped_column(String(128))
    house: Mapped[str | None] = mapped_column(String(32), nullable=True)
    apartment: Mapped[str | None] = mapped_column(String(32), nullable=True)

    # Geolocation
    latitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    longitude: Mapped[float | None] = mapped_column(Float, nullable=True)

    description: Mapped[str | None] = mapped_column(String(512), nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="addresses")  # type: ignore # noqa: F821
