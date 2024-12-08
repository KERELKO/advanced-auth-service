from loguru import logger
from src.core.dto.permissions import AddPermissionDTO
from src.core.dto.users import AddUserDTO
from tests import _container as container

from src.modules.authorization.service import AuthorizationService
from tests.conftest import disposable_data, registered_user


async def test_authorization_service(
    add_user_dto: AddUserDTO, add_permission_dto: AddPermissionDTO,
) -> None:
    async with disposable_data():
        async with registered_user(add_user_dto) as user:
            service = container.resolve(AuthorizationService)
            new_permission = await service.register_permission(add_permission_dto)
            logger.info(new_permission)

            user_permissions = await service.get_user_permissions(user.id)
            logger.info(user_permissions)
            assert new_permission not in user_permissions

            assert await service.has_permissions(
                user_id=user.id, permissions=set([new_permission.codename]),
            ) is False

            user_with_permssion = await service.grant_permissions(
                user.id, set([new_permission.codename]),
            )
            logger.info(user_with_permssion)

            assert new_permission in user_with_permssion.permissions

            assert await service.has_permissions(
                user_id=user.id, permissions=set([new_permission.codename]),
            ) is True
