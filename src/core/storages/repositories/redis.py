import json
from dataclasses import asdict

from redis.asyncio import Redis
from loguru import logger

from src.core.config import Config
from src.core.exceptions import ObjectDoesNotExist
from src.modules.mfa.dto import AddMFACode

from .base import AbstractCodeRepository


class RedisCodeRepository(AbstractCodeRepository):
    def __init__(self, config: Config) -> None:
        self._config = config
        self.redis = Redis.from_url(self._config.redis_url)

    async def set(self, dto: AddMFACode, ttl: int):
        data = asdict(dto)
        data.pop('user_id')
        await self.redis.set(str(dto.user_id), value=json.dumps(data), ex=ttl)
        logger.info(f'Set code for the user: user_id={dto.user_id}')

    async def get(self, user_id: int) -> AddMFACode:
        data: str | None = await self.redis.get(str(user_id))
        if not data:
            logger.info(f'Code does not exist: user_id={user_id}')
            raise ObjectDoesNotExist(user_id)
        return AddMFACode(user_id=user_id, **json.loads(data))
