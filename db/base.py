from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from core.config import settings


engine = create_async_engine(url=settings.database_connection, echo=False)
async_session = async_sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False
)


async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session


class Base(DeclarativeBase):
    pass
