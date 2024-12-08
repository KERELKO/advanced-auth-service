import pytest
from loguru import logger
from tests import _container as container

from src.core.dto.permissions import AddPermissionDTO
from src.core.dto.users import AddUserDTO
from src.core.exceptions import ObjectDoesNotExist
from src.core.storage.repositories.base import (
    IPermissionRepository,
    IUserRepository,
)
from src.core.storage.repositories.sqlalchemy import (
    SQLAlchemyPermissionRepository,
    SQLAlchemyUserRepository,
)

from .conftest import disposable_data


async def test_add_and_get_methods_of_user_repository(add_user_dto: AddUserDTO) -> None:
    async with disposable_data():
        repo = container.resolve(IUserRepository)
        assert isinstance(repo, SQLAlchemyUserRepository)

        added_user = await repo.add(add_user_dto)

        assert added_user.id is not None

        assert added_user.username == add_user_dto.username

        user = await repo.get(id=added_user.id)

        assert user.hashed_password == add_user_dto.hashed_password

        with pytest.raises(ObjectDoesNotExist):
            user = await repo.get(id=-1)


async def test_add_and_get_methods_of_permission_repository(
    add_permission_dto: AddPermissionDTO,
) -> None:
    async with disposable_data():
        # user_repo = container.resolve(IUserRepository)
        repo = container.resolve(IPermissionRepository)
        assert isinstance(repo, SQLAlchemyPermissionRepository)

        added_permission = await repo.add(add_permission_dto)
        logger.info(added_permission)

        assert added_permission.id is not None

        assert added_permission.codename == add_permission_dto.codename

        permission_1 = await repo.get_by_codename(codename=add_permission_dto.codename)
        logger.info(permission_1)

        assert permission_1.id == added_permission.id

        permission_2 = await repo.get(id=added_permission.id)
        logger.debug(f'{permission_1}:{permission_2}')

        assert permission_2 == permission_1

        # added_user = await user_repo.add(AddUserDTO('asdasdasd', email='asdasd@gmailcom'))
