import pytest
from tests.conftest import (
    add_user_dto,
    register_user_dto,
)


register_user_dto = pytest.fixture()(register_user_dto)

add_user_dto = pytest.fixture()(add_user_dto)
