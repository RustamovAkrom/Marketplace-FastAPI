import enum

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.sqltypes import String

from db.base import BaseModel


class UserRole(str, enum.Enum):
    admin = "admin"
    seller = "seller"
    buyer = "buyer"


class User(BaseModel):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    full_name: Mapped[str | None] = mapped_column(String(255), nullable=True)

    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    is_superuser: Mapped[bool] = mapped_column(nullable=False, default=False)
    is_verified: Mapped[bool] = mapped_column(nullable=False, default=False)

    role: Mapped[UserRole] = mapped_column(
        String(50), nullable=False, default=UserRole.buyer
    )
    orders: Mapped[list["Order"]] = relationship(back_populates="user")  # type: ignore # noqa: F821

    def __repr__(self):
        return f"<User id={self.id} email={self.email} full_name={self.full_name}>"
