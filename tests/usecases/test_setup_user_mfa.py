from loguru import logger
from tests import _container as container
from tests.conftest import (
    disposable_data,
    registered_user,
)

from src.modules.mfa.dto import UpdateUserMFA
from src.usecases.mfa import SetupUserMFA


async def test_can_enable_user_mfa(add_user_dto):
    async with disposable_data():
        async with registered_user(add_user_dto) as user:
            setup_user_mfa = container.resolve(SetupUserMFA)

            updated_user = await setup_user_mfa(
                UpdateUserMFA(user_id=user.id, mfa_enabled=True, mfa_type='otp'),
            )
            logger.info(updated_user)

            assert updated_user.mfa_type == 'otp'
            assert updated_user.mfa_enabled is True
            assert updated_user.mfa_secret is not None
