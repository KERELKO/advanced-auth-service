from loguru import logger
from tests import _container as container
from tests.conftest import disposable_data

from src.modules.authentication.dto import (
    LoginUserDTO,
    RegisterUserDTO,
)
from src.usecases.auth import (
    LoginUser,
    RegisterUser,
)


async def test_login_user_usecase(register_user_dto: RegisterUserDTO):
    async with disposable_data():
        login_user = container.resolve(LoginUser)
        register_user = container.resolve(RegisterUser)

        user = await register_user(register_user_dto)
        logger.info(user)

        result = await login_user(
            LoginUserDTO(username=user.username, password=register_user_dto.password)
        )

        if isinstance(result, tuple):
            access_token, refresh_token = result
        else:
            assert False, 'MFA isnt suppose to be here'
        logger.info(f'Access token: {access_token}\nRefresh token: {refresh_token}')

        assert True
