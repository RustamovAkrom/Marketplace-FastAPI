from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from db.base import BaseModel


class PromoCode(BaseModel):
    __tablename__ = "promo_codes"
    code: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, index=True
    )
    discount_percent: Mapped[int] = mapped_column(Integer, default=0)
    discount_amount: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    valid_from: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    valid_to: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
