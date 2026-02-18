from __future__ import annotations

from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class DeliveryStatus(str, Enum):
    created = "created"
    in_transit = "in_transit"
    delivered = "delivered"
    delayed = "delayed"
    canceled = "canceled"


class DeliveryCreate(BaseModel):
    driver_name: str = Field(min_length=1, max_length=80)
    status: DeliveryStatus = DeliveryStatus.created
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class Delivery(DeliveryCreate):
    id: str = Field(min_length=1, max_length=64)
