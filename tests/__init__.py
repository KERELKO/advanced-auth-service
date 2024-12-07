from contextlib import asynccontextmanager
from typing import AsyncGenerator

import punq
import pytest
from faker import Faker

from src.core import config
from src.core.config import Config
from src.core.di import Container
from src.core.dto.users import AddUserDTO, UserDTO
from src.core.storage.orm.db import Database
from src.core.storage.repositories.sqlalchemy import SQLAlchemyUserRepository
from src.modules.authentication.dto import LoginUserDTO, RegisterUserDTO
from src.modules.authentication.service import AuthenticationService

_container = Container()

faker = Faker()


@pytest.fixture
def register_user_dto() -> RegisterUserDTO:
    return RegisterUserDTO(
        username=faker.user_name(),
        email=faker.email(),
        password=faker.password(),
    )


@pytest.fixture
def container() -> Container:
    global _container
    return _container


@asynccontextmanager
async def registered_user(container: Container, register_user_dto) -> AsyncGenerator[UserDTO, None]:
    service = container.resolve(AuthenticationService)
    try:
        user_dto = await service.register(register_user_dto)
        yield user_dto
    finally:
        ...
