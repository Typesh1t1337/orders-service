import asyncio

import dramatiq
from dramatiq.brokers.redis import RedisBroker
from core.config import settings

redis_broker = RedisBroker(
    url=settings.redis_connection,
)

dramatiq.set_broker(redis_broker)


@dramatiq.actor
def send_email(user_id: int) -> None:
    asyncio.run(do_work(user_id))


async def do_work(user_id) -> None:
    await asyncio.sleep(10)
    print(f"Sending email to {user_id}")