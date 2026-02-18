from __future__ import annotations

from threading import Lock
from typing import Dict, List, Optional

from .models import Delivery, DeliveryCreate


class DeliveryStore:
    def __init__(self) -> None:
        self._lock = Lock()
        self._deliveries: Dict[str, Delivery] = {}

    def create(self, delivery_id: str, payload: DeliveryCreate) -> Delivery:
        delivery = Delivery(id=delivery_id, **payload.model_dump())
        with self._lock:
            self._deliveries[delivery_id] = delivery
        return delivery

    def get(self, delivery_id: str) -> Optional[Delivery]:
        with self._lock:
            return self._deliveries.get(delivery_id)

    def list(self) -> List[Delivery]:
        with self._lock:
            return list(self._deliveries.values())

    def delete(self, delivery_id: str) -> bool:
        with self._lock:
            return self._deliveries.pop(delivery_id, None) is not None
