import pytest
from tests.conftest import register_user_dto


register_user_dto = pytest.fixture()(register_user_dto)
