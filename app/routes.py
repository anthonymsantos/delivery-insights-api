from uuid import uuid4
from fastapi import APIRouter, HTTPException, status

from .db import SessionLocal
from .models import Delivery, DeliveryCreate
from .repository import DeliveryRepository

router = APIRouter(prefix="/deliveries", tags=["deliveries"])
repo = DeliveryRepository()


@router.post("", response_model=Delivery, status_code=status.HTTP_201_CREATED)
def create_delivery(payload: DeliveryCreate) -> Delivery:
    db = SessionLocal()
    try:
        return repo.create(db, uuid4().hex, payload)
    finally:
        db.close()


@router.get("", response_model=list[Delivery])
def list_deliveries():
    db = SessionLocal()
    try:
        return repo.list(db)
    finally:
        db.close()


@router.get("/{delivery_id}", response_model=Delivery)
def get_delivery(delivery_id: str):
    db = SessionLocal()
    try:
        delivery = repo.get(db, delivery_id)
    finally:
        db.close()

    if not delivery:
        raise HTTPException(status_code=404, detail="Delivery not found")

    return delivery


@router.delete("/{delivery_id}")
def delete_delivery(delivery_id: str):
    db = SessionLocal()
    try:
        deleted = repo.delete(db, delivery_id)
    finally:
        db.close()

    if not deleted:
        raise HTTPException(status_code=404, detail="Delivery not found")

    return {"deleted": True}