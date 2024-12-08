from contextlib import asynccontextmanager
import random
from typing import AsyncGenerator

import pytest
from faker import Faker
from sqlalchemy import text
from src.core.dto.permissions import AddPermissionDTO
from tests import _container as container

from src.core.dto.users import (
    AddUserDTO,
    UserDTO,
)
from src.core.storage.orm.db import Database
from src.core.storage.repositories.base import IUserRepository
from src.core.storage.repositories.sqlalchemy import SQLAlchemyUserRepository
from src.modules.authentication.dto import RegisterUserDTO


faker = Faker()


@pytest.fixture
def add_user_dto() -> AddUserDTO:
    return AddUserDTO(
        username=faker.user_name(),
        email=faker.email(),
        hashed_password=str(hash(faker.password())),
    )


@pytest.fixture
def register_user_dto() -> RegisterUserDTO:
    return RegisterUserDTO(
        username=faker.user_name(),
        email=faker.email(),
        password=faker.password(),
    )


@pytest.fixture
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
