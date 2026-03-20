from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app import db

from .models import Delivery, DeliveryCreate, DeliveryUpdate
from .orm_models import DeliveryORM


class DeliveryRepository:
    def create(self, db: Session, delivery_id: str, payload: DeliveryCreate) -> Delivery:
        row = DeliveryORM(
            id=delivery_id,
            driver_name=payload.driver_name,
            status=payload.status.value,
            timestamp=payload.timestamp,
        )

        db.add(row)
        db.commit()
        db.refresh(row)

        return Delivery(
            id=row.id,
            driver_name=row.driver_name,
            status=row.status,
            timestamp=row.timestamp,
        )

    def get(self, db: Session, delivery_id: str) -> Optional[Delivery]:
        row = db.get(DeliveryORM, delivery_id)
        if row is None:
            return None

        return Delivery(
            id=row.id,
            driver_name=row.driver_name,
            status=row.status,
            timestamp=row.timestamp,
        )

    def list(
        self,
        db: Session,
        limit: int = 10,
        offset: int = 0,
        status: str | None = None,
        driver_name: str | None = None,
    ) -> list[Delivery]:
        stmt = select(DeliveryORM)

        if status:
            stmt = stmt.where(DeliveryORM.status == status)

        if driver_name:
            stmt = stmt.where(DeliveryORM.driver_name.ilike(f"%{driver_name}%"))

        stmt = stmt.offset(offset).limit(limit)

        rows = db.scalars(stmt).all()

        return [
            Delivery(
                id=row.id,
                driver_name=row.driver_name,
                status=row.status,
                timestamp=row.timestamp,
            )
            for row in rows
        ]

    def delete(self, db: Session, delivery_id: str) -> bool:
        row = db.get(DeliveryORM, delivery_id)
        if row is None:
            return False

        db.delete(row)
        db.commit()
        return True
    
    def update(
        self,
        db: Session,
        delivery_id: str,
        payload: DeliveryUpdate,
    ) -> Optional[Delivery]:
        row = db.get(DeliveryORM, delivery_id)
        if row is None:
            return None

        row.driver_name = payload.driver_name
        row.status = payload.status.value

        db.commit()
        db.refresh(row)

        return Delivery(
            id=row.id,
            driver_name=row.driver_name,
            status=row.status,
            timestamp=row.timestamp,
        )    