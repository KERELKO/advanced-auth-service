from pathlib import Path
from loguru import logger
from src.core.dto.users import UpdateUserDTO, UserDTO
from src.core.storage.repositories.base import IUserRepository
from src.modules.mfa.service import MFAService
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


async def test_login_user_with_mfa_usecase(register_user_dto: RegisterUserDTO):
    async with disposable_data():
        user_repo = container.resolve(IUserRepository)
        mfa_service = container.resolve(MFAService)
        login_user = container.resolve(LoginUser)
        register_user = container.resolve(RegisterUser)

        user = await register_user(register_user_dto)
        logger.info(user)
        assert user.mfa_secret is not None

        if user.mfa_enabled is False:
            await user_repo.update(user.id, UpdateUserDTO(mfa_enabled=True))

        user: UserDTO = await login_user(  # type: ignore
            LoginUserDTO(username=user.username, password=register_user_dto.password)
        )

        if isinstance(user, tuple):
            assert False, 'MFA required for the test, but get tokens without it'

        assert user.mfa_secret is not None
        assert user.email is not None

        qrcode_file = Path(__file__).parent / 'qrcode.png'
        mfa_service.generate_otp_uri(
            user.mfa_secret, name=user.email, filepath=qrcode_file,
        )

        assert qrcode_file.exists() is True

        code = input(
            '#'*70 + '\n'
            '# Open your authenticator and scan QR code from the created file.\n'
            f'# ({qrcode_file})\n'
            '# Enter 6-digits code: '
        )
        qrcode_file.unlink()

        access_token, refresh_token = await login_user.verify_mfa_code(user, code)

        logger.info(f'Access token: {access_token}\nRefresh token: {refresh_token}')
        assert True
