# src/db/crud/payment.py
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.payments import Payment


class PaymentCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self, order_id: int, amount: float, currency: str = "USD"
    ) -> Payment:
        p = Payment(
            order_id=order_id, amount=amount, currency=currency, status="created"
        )
        self.session.add(p)
        await self.session.commit()
        await self.session.refresh(p)
        return p

    async def update_intent(self, payment: Payment, intent_id: str, status: str):
        payment.stripe_payment_intent = intent_id
        payment.status = status
        self.session.add(payment)
        await self.session.commit()
        await self.session.refresh(payment)
        return payment

    async def mark_succeeded(self, payment: Payment):
        payment.succeeded = True
        payment.status = "succeeded"
        self.session.add(payment)
        await self.session.commit()
        await self.session.refresh(payment)
        return payment

    async def get_by_intent(self, intent_id: str) -> Payment | None:
        stmt = select(Payment).where(Payment.stripe_payment_intent == intent_id)
        res = await self.session.execute(stmt)
        return res.scalars().first()

    async def get(self, payment_id: int) -> Payment:
        obj = await self.session.get(Payment, payment_id)
        if not obj:
            raise HTTPException(404, "Payment not found")
        return obj
