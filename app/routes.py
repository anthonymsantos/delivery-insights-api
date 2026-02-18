from __future__ import annotations

from uuid import uuid4
from fastapi import APIRouter, HTTPException, status

from .models import Delivery, DeliveryCreate
from .store import DeliveryStore

router = APIRouter(prefix="/deliveries", tags=["deliveries"])
store = DeliveryStore()


@router.post("", response_model=Delivery, status_code=status.HTTP_201_CREATED)
def create_delivery(payload: DeliveryCreate) -> Delivery:
    delivery_id = uuid4().hex
    return store.create(delivery_id=delivery_id, payload=payload)


@router.get("", response_model=list[Delivery])
def list_deliveries() -> list[Delivery]:
    return store.list()


@router.get("/{delivery_id}", response_model=Delivery)
def get_delivery(delivery_id: str) -> Delivery:
    delivery = store.get(delivery_id)
    if delivery is None:
        raise HTTPException(status_code=404, detail="Delivery not found")
    return delivery


@router.delete("/{delivery_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_delivery(delivery_id: str) -> None:
    deleted = store.delete(delivery_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Delivery not found")
    return None
