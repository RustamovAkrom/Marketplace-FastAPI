from sqlalchemy import Boolean, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from db.base import BaseModel


class PromoCode(BaseModel):
    __tablename__ = "promo_codes"

    code: Mapped[str] = mapped_column(String(50), unique=True)
    discount_percent: Mapped[int] = mapped_column(Integer, default=0)
    discount_amount: Mapped[float | None] = mapped_column(Numeric(10, 2))

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    def __repr__(self):
        return f"<PromoCode(code={self.code}, discount_percent={self.discount_percent}, discount_amount={self.discount_amount}, is_active={self.is_active})>"


__all__ = ("PromoCode",)
