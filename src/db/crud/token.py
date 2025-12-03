from datetime import datetime
from typing import Optional

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.revoked_token import RevokedToken


class TokenCRUD:
    def __init__(self, sessino: AsyncSession) -> None:
        self.sessino = sessino

    async def add(
        self,
        jti: str,
        token_type: str,
        expires_at: datetime,
        user_id: Optional[int] = None,
    ) -> None:
        revoked = RevokedToken(
            jti=jti, token_type=token_type, expires_at=expires_at, user_id=user_id
        )
        self.sessino.add(revoked)
        await self.sessino.commit()

    async def exists(self, jti: str) -> bool:
        stmt = await self.sessino.execute(
            select(RevokedToken).where(RevokedToken.jti == jti)
        )
        return stmt.scalar_one_or_none() is not None

    async def cleanup_expired(self) -> int:
        now = datetime.utcnow()
        stmt = delete(RevokedToken).where(RevokedToken.expires_at < now)
        res = await self.sessino.execute(stmt)
        await self.sessino.commit()
        # The result.rowcount may be driver-dependent; we return 0/1+ best-effort
        return getattr(res, "rowcount", 0)
