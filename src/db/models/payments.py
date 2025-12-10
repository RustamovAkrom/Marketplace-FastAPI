# src/db/models/payments.py
from __future__ import annotations

from sqlalchemy import Boolean, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import BaseModel


class Payment(BaseModel):
    __tablename__ = "payments"

    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), index=True)
    stripe_payment_intent: Mapped[str | None] = mapped_column(
        String(255), nullable=True, index=True
    )
    amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(10), nullable=False, default="USD")
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="created")
    succeeded: Mapped[bool] = mapped_column(Boolean, default=False)

    order: Mapped["Order"] = relationship("Order")  # type: ignore # noqa: F821
