# src/db/models/revoked_token.py
from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from db.base import BaseModel


class RevokedToken(BaseModel):
    __tablename__ = "revoked_tokens"

    jti: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False
    )
    token_type: Mapped[str] = mapped_column(
        String(20), nullable=False
    )  # 'access' or 'refresh'
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    # optional: store user_id to implement "logout_all"
    user_id: Mapped[int | None] = mapped_column(Integer, nullable=True, index=True)

    def __repr__(self) -> str:
        return f"<RevokedToken(jti={self.jti} type={self.token_type} expires_at={self.expires_at})>"


__all__ = ("RevokedToken",)
