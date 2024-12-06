import pytest

from src.core.dto.users import AddUserDTO
from src.core.exceptions import ObjectDoesNotExist
from src.core.storage.repositories.sqlalchemy import SQLAlchemyUserRepository
from src.core.storage.repositories.base import IUserRepository

from tests import _container as container


async def test_can_add_and_get_methods_of_repository() -> None:
    repo = container.resolve(IUserRepository)
    assert isinstance(repo, SQLAlchemyUserRepository)

    dto = AddUserDTO(username='admin', email='admin@gmail.com', hashed_password='lalal')

    added_user = await repo.add(dto)

    assert added_user.id is not None

    assert added_user.username == dto.username

    user = await repo.get(id=added_user.id)

    assert user.hashed_password == dto.hashed_password

    with pytest.raises(ObjectDoesNotExist):
        user = await repo.get(id=-1)
