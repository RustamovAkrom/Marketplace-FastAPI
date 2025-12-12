from fastapi import APIRouter, Body, Depends, HTTPException

from schemas.auth import (
    TokenScheme,
)
from services.auth_service import VerificationService, get_verification_service

router = APIRouter()


@router.post("/verify")
async def verify(
    type_: str = Body(..., embed=True),  # "email" or "phone"
    data: TokenScheme = Body(...),
    verification_service: VerificationService = Depends(get_verification_service),
) -> dict:
    if type_ == "email":
        return await verification_service.verify_email(data.token)
    elif type_ == "phone":
        return await verification_service.verify_phone(data.token)
    else:
        raise HTTPException(status_code=400, detail="Invalid verification type")


@router.post("/resend-verification")
async def resend_verification(
    user_id: int = Body(...),
    type_: str = Body(...),
    verification_service: VerificationService = Depends(get_verification_service),
):
    """
    Resend email or phone verification token
    """
    return await verification_service.resend_verification(user_id, type_)
