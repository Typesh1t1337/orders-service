from fastapi import HTTPException
from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from db.models.orders import Order
from db.models.orders import Status


class OrdersRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, item_id: int, user_id: int) -> Order:
        new_order = Order(item_id=item_id, user_id=user_id)
        self.session.add(new_order)
        await self.session.commit()
        await self.session.refresh(new_order)

        return new_order

    async def get_by_id(self, item_id: int, user_id: int) -> Order | None:
        query = await self.session.execute(select(Order).where(Order.item_id == item_id & Order.user_id == user_id))
        order = query.scalar_one_or_none()

        return order

    async def get_by_user_id(self, user_id: int) -> Sequence[Order] | None:
        query = await self.session.execute(select(Order).where(Order.user_id == user_id))
        orders = query.scalars().all()

        return orders

    async def update(self, user_id: int, item_id: int, status: Status) -> None:
        stmt = await self.session.execute(select(Order).where(Order.user_id == user_id & Order.item_id == item_id))
        order = stmt.scalar_one_or_none()

        if order is None:
            raise HTTPException(
                status_code=404, detail={
                    "message": "Order not found",
                }
            )

        order.status = status
        await self.session.commit()




