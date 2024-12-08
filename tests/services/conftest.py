import pytest

from tests.conftest import register_user_dto, add_permission_dto, add_user_dto


register_user_dto = pytest.fixture()(register_user_dto)


add_permission_dto = pytest.fixture()(add_permission_dto)


add_user_dto = pytest.fixture()(add_user_dto)
