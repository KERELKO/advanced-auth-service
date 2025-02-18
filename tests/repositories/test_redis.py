import datetime

from loguru import logger
from tests import _container as container

from src.core.storages.repositories.base import AbstractCodeRepository
from src.core.storages.repositories.redis import RedisCodeRepository
from src.modules.mfa.dto import AddMFACode


async def test_can_get_and_set_codes_in_redis_code_repository() -> None:
    repo = container.resolve(AbstractCodeRepository)

    assert isinstance(repo, RedisCodeRepository)

    dto = AddMFACode(user_id=1, expires_at=int(datetime.datetime.now().timestamp()), code='TEST')
    logger.info(dto)

    await repo.set(dto, ttl=15 * 60)

    code = await repo.get(dto.user_id)
    logger.info(code)

    assert code is not None

    assert code is not None
