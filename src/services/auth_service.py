from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import APIException
from core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from core.settings import settings
from db.crud.token import TokenCRUD
from db.crud.user import UserCRUD
from db.dependencies.sessions import get_db_session
from schemas.auth import (
    LoginOutScheme,
    LoginScheme,
    LogoutResponseScheme,
    LogoutScheme,
    RegisterOutScheme,
    RegistrationScheme,
    TokenResponseScheme,
)
from tasks.user_tasks import (
    send_email_verification_task,
    send_phone_verification_task,
)


class AuthService:
    def __init__(
        self,
        session: AsyncSession = Depends(get_db_session),
    ):
        self.session = session
        self.user_crud = UserCRUD(self.session)
        self.token_crud = TokenCRUD(self.session)

    async def register(self, data: RegistrationScheme) -> RegisterOutScheme:

        if await self.user_crud.get_by_email(data.email):
            raise APIException(
                "Email already registered", status_code=status.HTTP_400_BAD_REQUEST
            )

        if await self.user_crud.get_by_username(data.username):
            raise APIException(
                "Username already taken", status_code=status.HTTP_409_CONFLICT
            )

        if await self.user_crud.get_by_phone(data.phone):
            raise APIException(
                "Phone number already taken", status_code=status.HTTP_400_BAD_REQUEST
            )

        hashed_password = hash_password(data.password)
        user = await self.user_crud.create(data, hashed_password)

        token = create_access_token(
            subject=user.id,
            expires_delta=timedelta(
                minutes=settings.PASSWORD_RESET_TOKEN_EXPIRE_MINUTES
            ),
            extra={"type": "email_verification"},
        )

        if settings.ENV == "prod":
            # Send verification email to background
            await send_email_verification_task.delay(user.email, token)

        return RegisterOutScheme.model_validate(user)

    async def login(self, data: LoginScheme) -> LoginOutScheme:
        user = await self.user_crud.get_by_email(
            data.username
        ) or await self.user_crud.get_by_username(data.username)

        if not user:
            raise APIException(
                "Invalid credentials, username not found!",
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        if not verify_password(data.password, user.hashed_password):
            raise APIException(
                "Invalid credentials, password didn't match!",
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        # create tokens using subject (user id) to avoid nested 'sub' fields
        access_token = create_access_token(subject=user.id)
        refresh_token = create_refresh_token(subject=user.id)

        tokens = TokenResponseScheme(
            access_token=access_token, refresh_token=refresh_token
        )

        return LoginOutScheme(
            user=RegisterOutScheme.model_validate(user), tokens=tokens
        )

    async def logout(self, data: LogoutScheme) -> LogoutResponseScheme:
        try:
            payload = decode_token(data.refresh_token)
        except ValueError:
            return LogoutResponseScheme(detail="Token invalid or expired")

        if payload.get("type") != "refresh":
            raise APIException(
                "Provided toke is not a refresh token",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        jti = payload.get("jti")
        if not jti:
            return LogoutResponseScheme(detail="Invalid refresh token")

        if await self.token_crud.exists(jti):
            return LogoutResponseScheme(detail="Already logged out")

        exp_ts = payload.get("exp")
        expires_at = datetime.utcfromtimestamp(exp_ts) if exp_ts else datetime.utcnow()

        user_id = int(payload.get("sub")) if payload.get("sub") else None

        await self.token_crud.add(
            jti=jti, token_type="refresh", expires_at=expires_at, user_id=user_id
        )

        return LogoutResponseScheme(detail="Successfully logged out")

    async def refresh_access_token(self, refresh_token: str) -> dict:
        """
        Issue new access token using valid refresh token
        """

        try:
            payload = decode_token(refresh_token)
        except Exception:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")

        user_id = int(payload.get("sub"))
        user = await self.user_crud.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        access_token = create_access_token(
            subject=user.id,
            expires_delta=timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES),
            extra={"type": "access"},
        )
        return {"access_token": access_token, "token_type": "bearer"}

    async def verify_email(self, token: str) -> dict:
        """
        Verify email using a token (from email link)
        """

        try:
            payload = decode_token(token)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid token or expired")

        if payload.get("type") != "email_verification":
            raise HTTPException(status_code=400, detail="Invalid token type")

        user_id = int(payload.get("sub"))
        user = await self.user_crud.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        await self.user_crud.mark_email_verified(user)
        return {"msg": "Email verified successfully"}

    async def verify_phone(self, token: str) -> dict:
        """
        Verify phone using a token (from SMS link/code)
        """

        try:
            payload = decode_token(token)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid token or expired")

        if payload.get("type") != "phone_verification":
            raise HTTPException(status_code=400, detail="Invalid token type")

        user_id = int(payload.get("sub"))
        user = await self.user_crud.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        await self.user_crud.mark_phone_verified(user)
        return {"msg": "Phone verified successfully"}

    async def resend_verification(self, user_id: int, type_: str) -> dict:
        """
        Resend verification token to user email or phone
        """

        user = await self.user_crud.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if type_ == "email":
            token = create_access_token(
                subject=user.id,
                expires_delta=timedelta(
                    minutes=settings.PASSWORD_RESET_TOKEN_EXPIRE_MINUTES
                ),
                extra={"type": "email_verification"},
            )

            if settings.ENV == "prod":
                # Send verification token
                await send_email_verification_task.delay(user.email, token)

            return {"msg": "Verification email sent", "token": token}

        elif type_ == "phone":
            token = create_access_token(
                subject=user.id,
                expires_delta=timedelta(
                    minutes=settings.PASSWORD_RESET_TOKEN_EXPIRE_MINUTES
                ),
                extra={"type": "phone_verification"},
            )

            if settings.ENV == "prod":
                # Simple numeric code
                code = "123456"  # Leater will add code generator function
                await send_phone_verification_task.delay(user.phone, code)

            return {"msg": "Verification SMS sent", "code": code}

            # TODO: send SMS with token

        else:
            raise HTTPException(status_code=400, detail="Invalid verification type")

        return {"msg": f"{type_.capitalize()} verification token sent", "token": token}


__all__ = ("AuthService",)
