from typing import Optional

from pydantic import BaseModel, ConfigDict


class AddressCreateScheme(BaseModel):
    country: str
    city: str
    street: str
    house: Optional[str] = None
    apartment: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    description: Optional[str] = None


class AddressOutScheme(BaseModel):
    id: int
    user_id: int
    country: str
    city: str
    street: str
    house: Optional[str] = None
    apartment: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
