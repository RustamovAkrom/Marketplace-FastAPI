# src/services/payment_service.py
from __future__ import annotations

import asyncio

import stripe
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from db.crud.order import OrderCRUD
from db.crud.payment import PaymentCRUD
from db.models.orders import OrderStatus


class PaymentService:
    def __init__(self, session: AsyncSession):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.api_version = settings.STRIPE_API_VERSION
        self.session = session
        self.payment_crud = PaymentCRUD(session)
        self.order_crud = OrderCRUD(session)

    async def create_payment_intent_for_order(
        self, order_id: int, currency: str = "USD", metadata: dict | None = None
    ):
        # получаем заказ, убеждаемся что он в pending_payment
        order = await self.order_crud.get_order(order_id)
        if not order:
            raise HTTPException(404, "Order not found")

        # создаём локальную запись Payment
        payment = await self.payment_crud.create(
            order_id=order_id, amount=float(order.total_amount), currency=currency
        )

        # stripe call — blocking. Выполи в executor для safety
        loop = asyncio.get_running_loop()
        try:
            intent = await loop.run_in_executor(
                None,
                lambda: stripe.PaymentIntent.create(
                    amount=int(float(payment.amount) * 100),  # cents
                    currency=payment.currency.lower(),
                    metadata={"order_id": str(order_id), **(metadata or {})},
                    # optionally: payment_method_types=["card"]
                ),
            )
        except Exception as e:
            # можно логировать
            raise HTTPException(500, f"Stripe error: {e}")

        # update our payment record with intent id
        await self.payment_crud.update_intent(
            payment, intent.id, status=intent.status or "created"
        )
        return {
            "client_secret": intent.client_secret,
            "payment_id": payment.id,
            "intent_id": intent.id,
        }

    async def handle_webhook_event(self, event: dict):
        # event is parsed stripe Event dict
        typ = event["type"]
        data = event["data"]["object"]

        # payment_intent.succeeded
        if typ == "payment_intent.succeeded":
            intent_id = data.get("id")
            payment = await self.payment_crud.get_by_intent(intent_id)
            if not payment:
                # optionally create record or log
                return {"status": "unknown_payment"}

            # mark payment succeeded
            await self.payment_crud.mark_succeeded(payment)

            # mark order as paid (call order service / crud)
            # using order_crud.set_order_status or on_payment_success
            order = await self.order_crud.get_order(payment.order_id)
            if order:
                await self.order_crud.set_order_status(order, OrderStatus.PAID.value)
                # optionally trigger assign courier:
                # from services.order_service import OrderService
                # os = OrderService(self.session)
                # await os.assign_courier(order.id)

            return {"status": "ok"}
        # handle other events as needed
        return {"status": "ignored", "type": typ}
