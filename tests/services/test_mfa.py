import asyncio
from loguru import logger
from tests import _container as container

from src.modules.mfa.service import MFAService


async def test_can_pass_mfa() -> None:
    service = container.resolve(MFAService)

    secret_key = service.generate_secret()
    logger.info(f'Generated secret key: {secret_key}')

    code = service.generate_one_time_password(secret_key)
    logger.info(f'Code: {code}')

    assert service.verify_mfa_code(secret_key, code) is True


async def test_cannot_pass_mfa() -> None:
    service = container.resolve(MFAService)

    secret_key = service.generate_secret()
    logger.info(f'Generated secret key: {secret_key}')

    code = service.generate_one_time_password(secret_key)
    logger.info(f'Code: {code}')

    logger.info(f'Wait for {(s := service.interval + 5)} seconds to check if code will be invalid')
    await asyncio.sleep(s)

    assert service.verify_mfa_code(secret_key, code) is False
