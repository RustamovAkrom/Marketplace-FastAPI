from datetime import timedelta

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.security import create_access_token, decode_token
from db.crud.token import TokenCRUD
from db.crud.user import UserCRUD
from db.dependencies.sessions import get_db_session
from schemas.auth import ForgotPasswordScheme, PasswordResetScheme


class PasswordService:
    def __init__(
        self,
        session: AsyncSession = Depends(get_db_session),
    ):
        self.session = session
        self.user_crud = UserCRUD(self.session)
        self.token_crud = TokenCRUD(self.session)

    async def forgot_password(self, data: ForgotPasswordScheme) -> dict:

        user = await self.user_crud.get_by_email(data.email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        reset_token = create_access_token(
            subject=user.id,
            expires_delta=timedelta(
                minutes=settings.PASSWORD_RESET_TOKEN_EXPIRE_MINUTES
            ),
            extra={"type": "password_reset"},
        )

        # TODO: sending email user with reset_token
        # Example: send_email(user.email, reset_token)

        return {"msg": "Password reset link sent", "token": reset_token}

    async def reset_password(self, data: PasswordResetScheme) -> dict:
        try:
            payload = decode_token(data.token)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid or expired token")

        if payload.get("type") != "password_reset":
            raise HTTPException(status_code=400, detail="Invalid token type")

        user_id = int(payload.get("sub"))
        user = await self.user_crud.get_by_id(user_id)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        await self.user_crud.update_password(user, data.new_password)
        return {"msg": "Password updated successfully"}
