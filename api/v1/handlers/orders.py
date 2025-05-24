from sqlalchemy.ext.asyncio import AsyncSession
from db.repositories.orders import OrdersRepository
from schemas.orders import OrderCreate, OrderRead
from fastapi import Depends
from dependencies.auth_dependency import auth_required
from db.base import get_db


async def create_order(order: OrderCreate,
                       user_id: int = Depends(auth_required),
                       db: AsyncSession = Depends(get_db)
                       ):

    item_id = order.item_id
    repository = OrdersRepository(session=db)
    new_order = await repository.create(item_id=item_id, user_id=user_id)

    serialized_data = OrderRead.model_validate(new_order).model_dump()

    return serialized_data
