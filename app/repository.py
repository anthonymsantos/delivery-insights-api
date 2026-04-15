from typing import List, Optional

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app import db

from .models import (
    Delivery,
    DeliveryCreate,
    DeliverySortField,
    DeliveryUpdate,
    SortOrder,
)

from .orm_models import DeliveryORM


class DeliveryRepository:
    def create(
        self,
        db: Session,
        delivery_id: str,
        payload: DeliveryCreate,
        user_id: int,
    ) -> Delivery:
        row = DeliveryORM(
            id=delivery_id,
            driver_name=payload.driver_name,
            status=payload.status.value,
            timestamp=payload.timestamp,
            user_id=user_id,
        )

        db.add(row)
        db.commit()
        db.refresh(row)

        return Delivery(
            id=row.id,
            driver_name=row.driver_name,
            status=row.status,
            timestamp=row.timestamp,
            user_id=row.user_id,
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
            user_id=row.user_id,
        )

    def list(
        self,
        db: Session,
        limit: int = 10,
        offset: int = 0,
        status: str | None = None,
        driver_name: str | None = None,
        sort_by: DeliverySortField = DeliverySortField.timestamp,
        sort_order: SortOrder = SortOrder.desc,
    ) -> tuple[list[Delivery], int]:
        stmt = select(DeliveryORM)

        if status:
            stmt = stmt.where(DeliveryORM.status == status)

        if driver_name:
            stmt = stmt.where(DeliveryORM.driver_name.ilike(f"%{driver_name}%"))

        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = db.scalar(count_stmt) or 0

        sort_column = getattr(DeliveryORM, sort_by.value)
        if sort_order == SortOrder.desc:
            stmt = stmt.order_by(sort_column.desc())
        else:
            stmt = stmt.order_by(sort_column.asc())

        stmt = stmt.offset(offset).limit(limit)

        rows = db.scalars(stmt).all()

        items = [
            Delivery(
                id=row.id,
                driver_name=row.driver_name,
                status=row.status,
                timestamp=row.timestamp,
                user_id=row.user_id,
            )
            for row in rows
        ]

        return items, total

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
            user_id=row.user_id,
        )    