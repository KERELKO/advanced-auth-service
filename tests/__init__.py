import pytest
from faker import Faker

from src.core.di import Container

_container = Container()

faker = Faker('en_US')


@pytest.fixture
def container() -> Container:
    global _container
    return _container
