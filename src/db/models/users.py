from __future__ import annotations

import enum

from sqlalchemy import Boolean, Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import BaseModel


class UserRole(str, enum.Enum):
    admin = "admin"
    seller = "seller"
    buyer = "buyer"
    courier = "courier"


class User(BaseModel):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False, index=True
    )
    username: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, index=True
    )
    full_name: Mapped[str | None] = mapped_column(String(255), nullable=True)

    phone: Mapped[str | None] = mapped_column(String(20), unique=True, nullable=True)

    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_email_verified: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False
    )
    is_phone_verified: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False
    )

    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, name="user_role_enum"),
        nullable=False,
        default=UserRole.buyer,
    )

    # relations
    orders: Mapped[list["Order"]] = relationship(  # type: ignore # noqa: F821
        back_populates="user", cascade="all, delete-orphan"
    )
    cart: Mapped["Cart"] = relationship(  # type: ignore # noqa: F821
        "Cart", back_populates="user", uselist=False
    )

    seller: Mapped["Seller"] = relationship(  # type: ignore # noqa: F821
        "Seller", back_populates="user", uselist=False
    )

    addresses: Mapped[list["DeliveryAddress"]] = relationship(  # type: ignore # noqa: F821
        back_populates="user", cascade="all, delete-orphan"
    )

    couriers: Mapped["Courier"] = relationship(  # type: ignore # noqa: F821
        "Courier", back_populates="user", uselist=False
    )

    def __repr__(self):
        return f"<User id={self.id} email={self.email} role={self.role}>"
