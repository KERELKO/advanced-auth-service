from loguru import logger
from tests import _container as container
from tests.conftest import disposable_data

from src.core.dto.users import (
    UpdateUserDTO,
)
from src.core.config import config
from src.core.storages.repositories.base import IUserRepository
from src.modules.authentication.dto import (
    LoginUserDTO,
    RegisterUserDTO,
)
from src.modules.mfa.dto import MFACode, MFARequired
from src.modules.mfa.exceptions import InvalidCodeException
from src.usecases.auth import (
    LoginUser,
    RegisterUser,
)
from src.usecases.mfa import LoginUserMFA, SendMFACode


MESSAGE = """
###################################################################
# On application email (APP_EMAIL_ADDRESS in .env file)           #
# was sent 6-digits verification code. You need to enter it       #
###################################################################
"""


async def test_login_user_with_code_mfa_usecase(register_user_dto: RegisterUserDTO):
    async with disposable_data():
        user_repo = container.resolve(IUserRepository)
        login_user = container.resolve(LoginUser)
        register_user = container.resolve(RegisterUser)
        login_user_mfa = container.resolve(LoginUserMFA)
        send_mfa_code = container.resolve(SendMFACode)

        user = await register_user(register_user_dto)
        logger.info(user)
        assert user.mfa_secret is not None

        if user.mfa_enabled is False:
            await user_repo.update(
                user.id, UpdateUserDTO(
                    mfa_enabled=True, mfa_type='code', email=config.email_address,
                ),
            )

        mfa_required: MFARequired = await login_user(  # type: ignore
            LoginUserDTO(username=user.username, password=register_user_dto.password)
        )

        if isinstance(mfa_required, tuple):
            assert False, 'MFA required for the test, but get tokens without it'

        print(MESSAGE)

        flag = True
        while flag:
            await send_mfa_code(mfa_required.user)
            code = input('Enter 6-digits code: ')
            try:
                access_token, refresh_token = await login_user_mfa(
                    MFACode(mfa_required.user.id, code=code, mfa_type='code')
                )
                flag = False
            except InvalidCodeException:
                logger.error('Invalid code. try again')

        logger.info(f'Access token: {access_token}\nRefresh token: {refresh_token}')
        assert True
