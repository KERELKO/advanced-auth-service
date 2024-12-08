import pytest
from tests.conftest import add_user_dto, add_permission_dto


add_user_dto = pytest.fixture()(add_user_dto)


add_permission_dto = pytest.fixture()(add_permission_dto)
