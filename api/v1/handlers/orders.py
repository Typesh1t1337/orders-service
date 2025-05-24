import json

import orjson
from sqlalchemy.ext.asyncio import AsyncSession
from db.repositories.orders import OrdersRepository
from schemas.orders import OrderCreate, OrderRead, OrderUpdate
from fastapi import Depends, HTTPException
from dependencies.auth_dependency import auth_required
from db.base import get_db
from core.redis_config import redis_client


async def create_order(order: OrderCreate,
                       user_id: int = Depends(auth_required),
                       db: AsyncSession = Depends(get_db)
                       ):

    item_id = order.item_id
    repository = OrdersRepository(session=db)
    new_order = await repository.create(item_id=item_id, user_id=user_id)

    serialized_data = OrderRead.model_validate(new_order).model_dump()

    await redis_client.delete(f"orders:{user_id}")

    return serialized_data


async def get_order_by_id(order_id: int,
                          user_id: int = Depends(auth_required),
                          db: AsyncSession = Depends(get_db)
                          ):
    redis_key = f"orders:{user_id}:{order_id}"
    data = await redis_client.get(redis_key)
    if data:
        return orjson.loads(data)

    repository = OrdersRepository(session=db)
    order = await repository.get_by_id(order_id=order_id, user_id=user_id)

    if order is None:
        raise HTTPException(status_code=404, detail={
            "message": "Order not found"
        })

    serialized_data = OrderRead.model_validate(order).model_dump()
    json_parse = orjson.dumps(serialized_data)
    await redis_client.set(redis_key, json_parse, ex=15*60)

    return serialized_data


async def get_orders_by_user_id(user_id: int = Depends(auth_required),
                                db: AsyncSession = Depends(get_db)
                                ):

    redis_key = f"orders:{user_id}"
    cached_data = await redis_client.get(redis_key)
    if cached_data:
        return orjson.loads(cached_data)

    repository = OrdersRepository(session=db)
    orders = await repository.get_by_user_id(user_id=user_id)

    serialized_data = [OrderRead.model_validate(items).model_dump() for items in orders]
    json_parse = orjson.dumps(serialized_data)
    await redis_client.set(redis_key, json_parse, ex=15*60)

    return serialized_data


async def update_order_by_id(
                             order: OrderUpdate,
                             user_id: int = Depends(auth_required),
                             db: AsyncSession = Depends(get_db)):
    redis_key = f"orders:{user_id}:{order.order_id}"

    repository = OrdersRepository(session=db)
    order = await repository.update(
        item_id=order.item_id,
        user_id=user_id,
        status=order.status
    )

    serialized_data = OrderRead.model_validate(order).model_dump()
    await redis_client.set(redis_key, json.dumps(serialized_data), ex=15*60)

    return serialized_data

