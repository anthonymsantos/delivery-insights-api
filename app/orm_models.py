from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, DateTime
from datetime import datetime


class Base(DeclarativeBase):
    pass


class DeliveryORM(Base):
    __tablename__ = "deliveries"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    driver_name: Mapped[str] = mapped_column(String(80), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    user_id: Mapped[int] = mapped_column(nullable=False)

class UserORM(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)