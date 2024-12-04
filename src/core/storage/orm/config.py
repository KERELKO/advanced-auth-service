import asyncio

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.core.config import Config

from .models.common import Base


class Database:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.engine = create_async_engine(config.postgres_connection_string)
        self.async_session_factory = async_sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )

    def init(self) -> None:
        asyncio.run(self.create())

    async def create(self) -> None:
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def drop(self) -> None:
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
