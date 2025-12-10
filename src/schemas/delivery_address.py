from typing import Optional

from pydantic import BaseModel, ConfigDict


class DeliveryAddressBase(BaseModel):
    fullname: str
    phone: str
    country: str
    city: str
    street: str
    house: Optional[str] = None
    apartment: Optional[str] = None
    zip_code: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    description: Optional[str] = None


class DeliveryAddressCreateScheme(DeliveryAddressBase):
    pass


class DeliveryAddressUpdateScheme(DeliveryAddressBase):
    pass


class DeliveryAddressOutScheme(DeliveryAddressBase):
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)
