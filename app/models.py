from __future__ import annotations

from datetime import UTC, datetime
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
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))


class Delivery(DeliveryCreate):
    id: str = Field(min_length=1, max_length=64)
    user_id: int

class DeliveryUpdate(BaseModel):
    driver_name: str = Field(min_length=1, max_length=80)
    status: DeliveryStatus

class DeliveryListResponse(BaseModel):
    items: list[Delivery]
    total: int
    limit: int
    offset: int

class DeliverySortField(str, Enum):
    timestamp = "timestamp"
    driver_name = "driver_name"
    status = "status"


class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"