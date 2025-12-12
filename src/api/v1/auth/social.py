from fastapi import APIRouter, Depends, Query

from services.social_auth_service import SocialAuthService, get_social_service

router = APIRouter(prefix="/social-auth", tags=["Social Auth"])


@router.get("/login/{provider}")
async def social_login(
    provider: str,
    code: str = Query(...),
    redirect_uri: str = Query(...),
    social_auth_service: SocialAuthService = Depends(get_social_service),
):
    tokens = await social_auth_service.login_or_register(provider, code, redirect_uri)
    return tokens
