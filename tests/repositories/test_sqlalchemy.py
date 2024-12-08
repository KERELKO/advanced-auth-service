import uuid
import pytest
from loguru import logger
from tests import _container as container, faker

from src.core.dto.permissions import AddPermissionDTO
from src.core.dto.users import AddUserDTO, UpdateUserDTO
from src.core.exceptions import ObjectDoesNotExist
from src.core.storage.repositories.base import (
    IPermissionRepository,
    IUserRepository,
)
from src.core.storage.repositories.sqlalchemy import (
    SQLAlchemyPermissionRepository,
    SQLAlchemyUserRepository,
)

from .conftest import db_user, disposable_data


@pytest.mark.skip
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


async def test_can_update_user(
    add_user_dto: AddUserDTO, add_permission_dto: AddPermissionDTO,
) -> None:
    async with disposable_data():
        async with db_user(add_user_dto) as user:
            user_repo = container.resolve(IUserRepository)
            permission_repo = container.resolve(IPermissionRepository)
            perm = await permission_repo.add(add_permission_dto)
            logger.info(f'User(username={user.username}, id={user.id})')

            update_user_dto = UpdateUserDTO(
                username=faker.user_name(),
                email=faker.email(),
                permissions=[perm.codename],
                hashed_password=str(uuid.uuid4()),
                mfa_enabled=True,
                mfa_secret=str(uuid.uuid4()),
                oauth_provider=faker.user_name(),
                oauth_provider_id=str(uuid.uuid4()),
            )
            user_dto = await user_repo.update(user_id=user.id, dto=update_user_dto)
            logger.info(user_dto)

            assert user.username != update_user_dto.username
            assert user_dto.permissions


@pytest.mark.skip
async def test_add_and_get_methods_of_permission_repository(
    add_permission_dto: AddPermissionDTO,
    add_user_dto: AddUserDTO,
) -> None:
    async with disposable_data():
        async with db_user(add_user_dto) as _:
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
