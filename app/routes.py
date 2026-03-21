from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from .db import get_db
from .models import Delivery, DeliveryCreate, DeliveryStatus, DeliveryUpdate
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
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    status: DeliveryStatus | None = Query(default=None),
    driver_name: str | None = Query(default=None),
    db: Session = Depends(get_db),
) -> list[Delivery]:
    driver_name = driver_name or None

    return repo.list(
        db=db,
        limit=limit,
        offset=offset,
        status=status.value if status else None,
        driver_name=driver_name,
    )


@router.get("/{delivery_id}", response_model=Delivery)
def get_delivery(
    delivery_id: str,
    db: Session = Depends(get_db),
) -> Delivery:
    delivery = repo.get(db, delivery_id)

    if not delivery:
        raise HTTPException(status_code=404, detail="Delivery not found")

    return delivery


@router.delete("/{delivery_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_delivery(
    delivery_id: str,
    db: Session = Depends(get_db),
) -> None:
    deleted = repo.delete(db, delivery_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Delivery not found")

    return None

@router.put("/{delivery_id}", response_model=Delivery)
def update_delivery(
    delivery_id: str,
    payload: DeliveryUpdate,
    db: Session = Depends(get_db),
) -> Delivery:
    updated = repo.update(db, delivery_id, payload)

    if not updated:
        raise HTTPException(status_code=404, detail="Delivery not found")

    return updated