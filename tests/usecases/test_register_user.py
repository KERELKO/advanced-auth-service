from loguru import logger
from tests import _container as container
from tests.conftest import disposable_data

from src.modules.authentication.dto import RegisterUserDTO
from src.modules.authorization.service import AuthorizationService
from src.usecases.auth import RegisterUser


async def test_register_user_usecase(register_user_dto: RegisterUserDTO) -> None:
    async with disposable_data():
        # Check if AuthorizationService set default permissions
        register_user_dto.permissions = None
        authorization_service = container.resolve(AuthorizationService)

        register_user = container.resolve(RegisterUser)

        user = await register_user(register_user_dto)

        logger.info(user)

        assert user.id is not None

        permisison_codes = [p.codename for p in user.permissions]
        logger.info(f'User permissions: {permisison_codes}')
        logger.info(f'Default permissions: {authorization_service.default_permission_set}')

        assert set(authorization_service.default_permission_set) == set(permisison_codes)
