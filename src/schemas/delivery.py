from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from db.models.delivery import DeliveryStatus


class DeliveryOutScheme(BaseModel):
    order_id: int
    courier_id: int
    address_id: int
    status: list[DeliveryStatus]
    assigned_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
