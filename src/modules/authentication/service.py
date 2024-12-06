from dataclasses import asdict
from datetime import datetime, timedelta, timezone

import jwt
from loguru import logger

from src.core.config import Config
from src.core.dto.tokens import Token, TokenPayload
from src.core.dto.users import AddUserDTO, UserDTO
from src.core.storage.repositories.base import IUserRepository

from .dto import LoginUserDTO, RegisterUserDTO


class AuthenticationService:
    def __init__(self, repository: IUserRepository, config: Config) -> None:
        self.repo = repository
        self._config = config
        self.context = config.crypto_context

    async def login(self, dto: LoginUserDTO) -> tuple[Token, Token]:
        """
        Verifies user data and return tuple containing access and refresh tokens
        """
        return Token(''), Token('')

    async def logout(self, access_token: str) -> bool:
        """
        Check if token is active and destroy it
        """
        return True

    async def refresh_token(self, access_token: str, refresh_token: str) -> tuple[Token, Token]:
        """
        Return new access and refresh tokens if refresh token is active, otherwise throw
        `InvalidTokenException`
        """
        return Token(''), Token('')

    async def is_valid_token(self, token: str) -> bool:
        """
        Check if provided token is still valid
        """
        return True

    async def register(self, dto: RegisterUserDTO) -> UserDTO:
        """Register new user"""
        hashed_password = self._get_password_hash(dto.password)
        data = asdict(dto)
        data.pop('password')
        data['hashed_password'] = hashed_password
        return await self.repo.add(AddUserDTO(**data))

    def create_token(
        self,
        payload: TokenPayload,
        expires_delta: timedelta,
    ) -> str:
        """Create new token based on application configuration"""
        to_encode = asdict(payload)
        expire = datetime.now(timezone.utc) + expires_delta
        to_encode.update({'exp': expire})
        encoded_jwt = jwt.encode(
            to_encode,
            self._config.secret_key,
            algorithm=self._config.algorithms[0],
        )
        return encoded_jwt

    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Hash plain password and check if it equal to the hashed one"""
        return self.context.verify(plain_password, hashed_password)

    def _get_password_hash(self, password: str) -> str:
        """Return hashed password according to the application crypto context"""
        return self.context.hash(password)

    def _decode_token(self, token: str) -> TokenPayload:
        """Decode token and return its payload"""
        data = jwt.decode(
            jwt=token,
            key=self._config.secret_key,
            algorithms=self._config.algorithms,
        )
        logger.info(data)
        return TokenPayload(**data)
