import stripe
from fastapi import APIRouter, Depends, Header, HTTPException, Request

from core.settings import settings
from services.payment_service import PaymentService, get_payment_service

router = APIRouter(prefix="/payments", tags=["Payments"])


# 1) create payment intent for order (returns client_secret)
@router.post("/{order_id}/create")
async def create_payment(
    order_id: int, service: PaymentService = Depends(get_payment_service)
):
    return await service.create_payment_intent_for_order(order_id)


# 2) webhook endpoint — Stripe will POST events here
# IMPORTANT: do NOT use regular body parsing for verification — read raw body bytes
@router.post("/webhook", status_code=200)
async def stripe_webhook(
    request: Request,
    stripe_signature: str | None = Header(None),
    service: PaymentService = Depends(get_payment_service),
):
    payload = await request.body()
    sig_header = stripe_signature or request.headers.get(
        "stripe-signature"
    )  # header name lowercase may occur
    if sig_header is None:
        raise HTTPException(status_code=400, detail="Missing stripe signature")

    try:
        event = stripe.Webhook.construct_event(
            payload=payload,
            sig_header=sig_header,
            secret=settings.STRIPE_WEBHOOK_SECRET,
        )
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Webhook error: {e}")

    # event is verified — handle it
    result = await service.handle_webhook_event(event)
    return result
