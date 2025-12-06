from datetime import datetime
from typing import Optional

from fastapi import Depends
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from db.dependencies.sessions import get_db_session
from db.models.revoked_tokens import RevokedToken


class TokenCRUD:
    def __init__(self, session: AsyncSession = Depends(get_db_session)) -> None:
        self.session = session

    async def create(
        self,
        jti: str,
        token_type: str,
        expires_at: datetime,
        user_id: Optional[int] = None,
    ) -> RevokedToken:
        revoked = RevokedToken(
            jti=jti, token_type=token_type, expires_at=expires_at, user_id=user_id
        )
        self.session.add(revoked)
        await self.session.commit()
        await self.session.refresh(revoked)
        return revoked

    async def exists(self, jti: str) -> bool:
        stmt = await self.session.execute(
            select(RevokedToken).where(RevokedToken.jti == jti)
        )
        return stmt.scalar_one_or_none() is not None

    async def cleanup_expired(self) -> int:
        now = datetime.utcnow()
        stmt = delete(RevokedToken).where(RevokedToken.expires_at < now)
        res = await self.session.execute(stmt)
        await self.session.commit()
        # The result.rowcount may be driver-dependent; we return 0/1+ best-effort
        return getattr(res, "rowcount", 0)
