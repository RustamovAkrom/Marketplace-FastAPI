from fastapi import Depends, HTTPException
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from core.security import create_access_token, create_refresh_token
from core.settings import settings
from db.crud.user import UserCRUD
from db.dependencies.sessions import get_db_session


class SocialAuthService:
    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session
        self.user_crud = UserCRUD(self.session)

    async def exchange_code_for_token(
        self, provider: str, code: str, redirect_uri: str
    ) -> str:
        cfg = settings.OAUTH_PROVIDERS.get(provider)
        if not cfg:
            raise HTTPException(400, f"Provider {provider} not supported")

        async with AsyncClient() as client:
            data = {
                "client_id": cfg["client_id"],
                "client_secret": cfg["client_secret"],
                "code": code,
                "redirect_uri": redirect_uri,
                "grant_type": "authorization_code",
            }

            # Google expects form-encoded
            resp = await client.post(cfg["token_url"], data=data)
            if resp.status_code != 200:
                # печатаем тело ошибки для отладки
                text = await resp.aread()
                raise HTTPException(
                    status_code=resp.status_code,
                    detail=f"Google token error: {text.decode()}",
                )

            token_data = resp.json()
            access_token = token_data.get("access_token")
            if not access_token:
                raise HTTPException(400, "Failed to get access token")
            return access_token

    async def get_user_info(self, provider: str, access_token: str) -> dict:
        cfg = settings.OAUTH_PROVIDERS.get(provider)
        async with AsyncClient() as client:
            headers = {"Authorization": f"Bearer {access_token}"}
            resp = await client.get(cfg["userinfo_url"], headers=headers)
        resp.raise_for_status()
        return resp.json()

    async def login_or_register(
        self, provider: str, code: str, redirect_uri: str
    ) -> dict:
        token = await self.exchange_code_for_token(provider, code, redirect_uri)
        user_info = await self.get_user_info(provider, token)

        # пример, для google: {"email": "...", "sub": "...", "name": "..."}
        email = user_info.get("email")
        if not email:
            raise HTTPException(400, "Cannot retrieve email from provider")

        user = await self.user_crud.get_by_email(email)
        if not user:
            # создаём пользователя если не существует
            user_data = {
                "email": email,
                "username": email.split("@")[0],
                "full_name": user_info.get("name"),
            }
            user = await self.user_crud.create(user_data)

        # создаём JWT для пользователя
        access = create_access_token(subject=user.id)
        refresh = create_refresh_token(subject=user.id)
        return {"access_token": access, "refresh_token": refresh}


async def get_social_service(
    session: AsyncSession = Depends(get_db_session),
) -> SocialAuthService:
    return SocialAuthService(session)
