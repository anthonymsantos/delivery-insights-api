from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import Delivery, DeliveryCreate
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

    def list(self, db: Session) -> List[Delivery]:
        rows = db.scalars(select(DeliveryORM)).all()
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