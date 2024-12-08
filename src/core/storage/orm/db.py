import asyncio
import re

from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from src.core.config import Config
from src.core.exceptions import ApplicationException

from .models.common import Base


class Database:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.engine = create_async_engine(
            config.postgres_connection_string,
            isolation_level='SERIALIZABLE',
        )
        self.session_factory = async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )
        self.clear_db = self.__clear_db

    async def __clear_db(self) -> None:
        if self.config.env != 'dev':
            raise ApplicationException('Cannot clear database in non DEV environment')
        async with self.engine.connect() as connection:
            await connection.execute(
                text('TRUNCATE TABLE permissions, permission_user, users RESTART IDENTITY CASCADE;')
            )
            await connection.commit()

    def init(self) -> None:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.create())
        if self.config.env == 'dev':
            loop.run_until_complete(self.insert_data())

    async def insert_data(self) -> None:
        async with self.engine.connect() as conn:
            with open('db_data.sql', 'r') as file:
                statements = re.split(r';\s*$', file.read(), flags=re.MULTILINE)
                for statement in statements:
                    if statement:
                        await conn.execute(text(statement))
                await conn.commit()

    async def create(self) -> None:
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def drop(self) -> None:
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
