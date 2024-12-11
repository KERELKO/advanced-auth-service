import random

from loguru import logger

from tests import (
    _container as container,
    faker,
)

from src.core.config import config
from src.core.services.interfaces import AbstractNotificationService
from src.core.services.notifications import EmailNotificationService


async def test_can_send_email():
    service = container.resolve(AbstractNotificationService)
    logger.info(f'{config.email_address}:{config.email_password}')

    assert isinstance(service, EmailNotificationService)

    await service.send(
        message=f'Your verification code: {random.randint(111_111, 999_999)}',
        subject=faker.user_name(),
        to=config.email_address,
    )

    assert True
