from dataclasses import asdict
from datetime import datetime, timedelta, timezone

import jwt
from loguru import logger

from src.core.config import Config
from src.core.storage.repositories.base import IPermissionRepository, IUserRepository
from src.core.utils import not_found
from src.modules.authorization.dto import TokenPayload


class AuthorizationService:
    def __init__(
        self,
        config: Config,
        user_repository: IUserRepository,
        permission_repository: IPermissionRepository,
    ) -> None:
        self._config = config
        self.user_repository = user_repository
        self.permission_repository = permission_repository

    async def has_permissions(self, user_id: int, permissions: set[str]) -> bool:
        user = await self.user_repository.get(id=user_id) or not_found(id=user_id)
        return user.permissions <= permissions

    def decode_token(self, token: str) -> TokenPayload:
        data = jwt.decode(
            jwt=token,
            key=self._config.secret_key,
            algorithms=self._config.algorithms,
        )
        logger.info(data)
        return TokenPayload(**data)

    def create_access_token(
        self,
        payload: TokenPayload,
        expires_delta: timedelta | None = None,
    ) -> str:
        to_encode = asdict(payload)
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(
                minutes=self._config.access_token_expire_minutes
            )
        to_encode.update({'exp': expire})
        encoded_jwt = jwt.encode(
            to_encode,
            self._config.secret_key,
            algorithm=self._config.algorithms[0],
        )
        return encoded_jwt
