from datetime import datetime
from sqlalchemy import Integer, DateTime, Enum, ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column, relationship
from db.base import Base
import enum


class Status(enum.Enum):
    NEW = 'NEW'
    PROCESSED = 'PROCESSED'
    DELIVERING = 'DELIVERING'
    SHIPPED = 'SHIPPED'
    CANCELLED = 'CANCELLED'


class Order(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, unique=True)
    user_id: Mapped[int] = mapped_column(Integer, index=True, nullable=False)
    item_id: Mapped[int] = mapped_column(Integer, index=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    status: Mapped[Status] = mapped_column(Enum(Status), default=Status.NEW)

    order_logs = relationship("OrderLog", back_populates='order', cascade='all, delete, delete-orphan')


class OrderLog(Base):
    __tablename__ = 'order_logs'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, unique=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), index=True)
    status: Mapped[Status] = mapped_column(Enum(Status), default=Status.NEW)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    order = relationship(Order, back_populates='order_logs')

