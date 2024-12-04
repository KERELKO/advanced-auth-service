import typing as t
from datetime import datetime
from datetime import timedelta, timezone

import jwt
from src.core.config import Config


class SecurityService:
    def __init__(self, config: Config) -> None:
        self._config = config
        self.context = config.crypto_context

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        return self.context.hash(password)

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
