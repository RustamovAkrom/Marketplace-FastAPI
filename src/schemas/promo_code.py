from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class PromoCodeBase(BaseModel):
    code: str
    discount_percent: int = 0
    discount_amount: Optional[float] = None
    is_active: bool = True
    valid_from: Optional[datetime] = None
    valid_to: Optional[datetime] = None


class PromoCodeCreateScheme(PromoCodeBase):
    pass


class PromoCodeUpdateScheme(PromoCodeBase):
    pass


class PromoCodeOutScheme(PromoCodeBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
