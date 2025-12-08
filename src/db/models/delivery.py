from __future__ import annotations

import enum
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import BaseModel


class DeliveryStatus(str, enum.Enum):
    pending = "pending"  # ждёт курьера
    assigned = "assigned"  # курьер назначен
    picking = "picking"  # курьер забирает товар
    delivering = "delivering"  # в пути
    delivered = "delivered"  # доставлено
    canceled = "canceled"  # отменено


class Delivery(BaseModel):
    __tablename__ = "deliveries"

    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), unique=True)
    courier_id: Mapped[int] = mapped_column(ForeignKey("couriers.id"))
    address_id: Mapped[int] = mapped_column(
        ForeignKey("delivery_addresses.id"), nullable=False
    )

    status: Mapped[DeliveryStatus] = mapped_column(
        Enum(DeliveryStatus, name="delivery_status_enum"),
        default=DeliveryStatus.pending,
        nullable=False,
    )

    assigned_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    delivered_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    order: Mapped["Order"] = relationship("Order", back_populates="delivery")  # type: ignore # noqa: F821
    courier: Mapped["Courier"] = relationship("Courier")  # type: ignore # noqa: F821
    address: Mapped["DeliveryAddress"] = relationship("DeliveryAddress")  # type: ignore # noqa: F821
