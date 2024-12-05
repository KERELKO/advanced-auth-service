import typing as t
from datetime import datetime, timedelta, timezone

import jwt

from src.core.config import Config
from src.core.security import SecurityService


class AuthorizationService:
    def __init__(
        self,
        config: Config,
        security_service: SecurityService,
    ) -> None:
        self._config = config
        self.__security_service = security_service

    def create_access_token(
        self,
        data: dict[str, t.Any],
        expires_delta: timedelta | None = None,
    ) -> str:
        to_encode = data.copy()
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
            algorithm=self._config.algorithm,
        )
        return encoded_jwt
