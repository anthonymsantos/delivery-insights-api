from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .db import get_db
from .models import Delivery, DeliveryCreate
from .repository import DeliveryRepository

router = APIRouter(prefix="/deliveries", tags=["deliveries"])
repo = DeliveryRepository()


@router.post("", response_model=Delivery, status_code=status.HTTP_201_CREATED)
def create_delivery(
    payload: DeliveryCreate,
    db: Session = Depends(get_db),
) -> Delivery:
    return repo.create(db, uuid4().hex, payload)


@router.get("", response_model=list[Delivery])
def list_deliveries(
    db: Session = Depends(get_db),
) -> list[Delivery]:
    return repo.list(db)


@router.get("/{delivery_id}", response_model=Delivery)
def get_delivery(
    delivery_id: str,
    db: Session = Depends(get_db),
) -> Delivery:
    delivery = repo.get(db, delivery_id)

    if not delivery:
        raise HTTPException(status_code=404, detail="Delivery not found")

    return delivery


@router.delete("/{delivery_id}")
def delete_delivery(
    delivery_id: str,
    db: Session = Depends(get_db),
):
    deleted = repo.delete(db, delivery_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Delivery not found")

    return {"deleted": True}