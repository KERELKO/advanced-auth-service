import asyncio
import random
from contextlib import asynccontextmanager
from typing import (
    AsyncGenerator,
    Generator,
)

import pytest
from sqlalchemy import text
from src.modules.authentication.dto import RegisterUserDTO
from tests import (
    _container as container,
    faker,
)

from src.core.dto.permissions import AddPermissionDTO
from src.core.dto.users import (
    AddUserDTO,
    UserDTO,
)
from src.core.storage.orm.db import Database
from src.core.storage.repositories.base import IUserRepository
from src.core.storage.repositories.sqlalchemy import SQLAlchemyUserRepository


@pytest.fixture(scope="session")
def event_loop(request) -> Generator:
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


def register_user_dto() -> RegisterUserDTO:
    return RegisterUserDTO(
        username=faker.user_name(),
        email=faker.email(),
        password=faker.password(),
    )


def add_user_dto() -> AddUserDTO:
    return AddUserDTO(
        username=faker.user_name(),
        email=faker.email(),
        hashed_password=str(hash(faker.password())),
    )


def add_permission_dto() -> AddPermissionDTO:
    action = random.choice(['Add', 'Remove', 'Update', 'Delete', 'Retrieve'])
    name = faker.user_name()
    return AddPermissionDTO(
        name=f'{action} {name}',
        codename=f'{action.lower()}_{name.lower()}'
    )


@asynccontextmanager
async def disposable_data() -> AsyncGenerator[None, None]:
    """Clear database after usage"""
    db = container.resolve(Database)
    try:
        yield None
    finally:
        await db.clear_db()
        await db.insert_data()


@asynccontextmanager
async def registered_user(add_user_dto: AddUserDTO) -> AsyncGenerator[UserDTO, None]:
    """Clear database after usage"""
    db = container.resolve(Database)
    repo = container.resolve(IUserRepository)
    assert isinstance(repo, SQLAlchemyUserRepository)
    try:
        added_user = await repo.add(add_user_dto)
        yield added_user
    finally:
        async with db.engine.connect() as conn:
            await conn.execute(text(f'DELETE FROM users WHERE users.id = {added_user.id}'))
            await conn.commit()
