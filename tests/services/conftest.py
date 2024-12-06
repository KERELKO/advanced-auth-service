import pytest
from faker import Faker

from src.modules.authentication.dto import RegisterUserDTO

faker = Faker()


@pytest.fixture
def register_user_dto() -> RegisterUserDTO:
    return RegisterUserDTO(
        username=faker.user_name(),
        email=faker.email(),
        password=faker.password(),
    )
