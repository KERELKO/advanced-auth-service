from contextlib import asynccontextmanager
from typing import AsyncGenerator

import pytest
from faker import Faker

from src.core.di import Container
from src.core.dto.users import (
    UserDTO,
)
from src.modules.authentication.dto import (
    RegisterUserDTO,
)
from src.modules.authentication.service import AuthenticationService


_container = Container()

faker = Faker('en_US')


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
