import enum

from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.sqltypes import Boolean, String

from db.base import BaseModel


class UserRole(str, enum.Enum):
    admin = "admin"
    seller = "seller"
    buyer = "buyer"


class User(BaseModel):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    full_name: Mapped[str | None] = mapped_column(String(255), nullable=True)

    phone: Mapped[str | None] = mapped_column(String(20), unique=True, nullable=True)

    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
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

    orders: Mapped[list["Order"]] = relationship(  # type: ignore # noqa: F821
        back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User id={self.id} email={self.email} role={self.role}>"
