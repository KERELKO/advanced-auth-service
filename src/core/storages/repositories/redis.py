import json
from dataclasses import asdict

import aioredis
from loguru import logger

from src.core.config import Config
from src.core.exceptions import ObjectDoesNotExist
from src.modules.mfa.dto import MFACode

from .base import AbstractCodeRepository


class RedisCodeRepository(AbstractCodeRepository):
    def __init__(self, config: Config) -> None:
        self._config = config
        self.redis = aioredis.from_url(self._config.redis_url)

    async def set(self, data: MFACode):
        _data = asdict(data)
        _data.pop('user_id')
        await self.redis.set(str(data.user_id), value=json.dumps(_data), ex=data.expires_at)
        logger.info(f'Set code for the user: user_id={data.user_id}')

    async def get(self, user_id: int) -> MFACode:
        data: str | None = await self.redis.get(str(user_id))
        if not data:
            logger.info(f'Code does not exist: user_id={user_id}')
            raise ObjectDoesNotExist(user_id)
        return MFACode(user_id=user_id, **json.loads(data))
