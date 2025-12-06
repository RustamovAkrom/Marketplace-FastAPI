from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from db.dependencies.sessions import get_db_session
from services.social_auth_service import SocialAuthService

router = APIRouter(prefix="/social-auth", tags=["Social Auth"])


async def get_social_service(
    session: AsyncSession = Depends(get_db_session),
) -> SocialAuthService:
    return SocialAuthService(session)


@router.get("/login/{provider}")
async def social_login(
    provider: str,
    code: str = Query(...),
    redirect_uri: str = Query(...),
    social_auth_service: SocialAuthService = Depends(get_social_service),
):
    tokens = await social_auth_service.login_or_register(provider, code, redirect_uri)
    return tokens
