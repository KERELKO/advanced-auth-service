from dataclasses import asdict
from datetime import datetime, timedelta

import jwt
from loguru import logger

from src.core.config import Config
from src.core.dto.tokens import Token, TokenPayload
from src.core.dto.users import AddUserDTO, UserDTO
from src.core.exceptions import InvalidTokenException, ObjectDoesNotExist
from src.core.storage.repositories.base import IUserRepository
from src.modules.authentication.exceptions import IncorrectPasswordException, TokenExpiredException

from .dto import LoginUserDTO, RegisterUserDTO


class AuthenticationService:
    def __init__(self, repository: IUserRepository, config: Config) -> None:
        self.repo = repository
        self._config = config
        self.context = config.crypto_context

    async def login(self, dto: LoginUserDTO) -> tuple[Token, Token]:
        """
        Verifies user data and return a tuple containing access and refresh tokens.
        """
        user = await self.repo.get_by_username(dto.username)

        if user is None:
            raise ObjectDoesNotExist(id=dto.username)

        # TODO: handle if hashed_password is None
        if not self._verify_password(dto.password, user.hashed_password):  # type: ignore
            raise IncorrectPasswordException()

        access_token_exp, refresh_token_exp = self.__create_tokens_exp()

        access_token_payload = TokenPayload(
            user_id=user.id,
            sub=user.username,
            exp=access_token_exp,
        )
        refresh_token_payload = TokenPayload(
            user_id=user.id,
            sub=user.username,
            exp=refresh_token_exp,
        )

        access_token = self.create_token(access_token_payload)
        refresh_token = self.create_token(refresh_token_payload)

        return Token(access_token), Token(refresh_token)

    async def refresh_token(self, refresh_token: str) -> tuple[Token, Token]:
        """
        Return new access and refresh tokens if refresh token is active, otherwise throw
        `InvalidTokenException`.
        """
        try:
            decoded_refresh_token = self._decode_token(refresh_token)
            if self._is_token_expired(decoded_refresh_token.exp):
                raise TokenExpiredException

            access_token_exp, refresh_token_exp = self.__create_tokens_exp()

            access_token_payload = TokenPayload(
                decoded_refresh_token.sub, decoded_refresh_token.user_id, exp=access_token_exp
            )
            refresh_token_payload = TokenPayload(
                decoded_refresh_token.sub, decoded_refresh_token.user_id, exp=refresh_token_exp
            )

            new_access_token = self.create_token(access_token_payload)
            new_refresh_token = self.create_token(refresh_token_payload)

            return Token(new_access_token), Token(new_refresh_token)

        except jwt.ExpiredSignatureError:
            raise TokenExpiredException
        except jwt.DecodeError:
            raise InvalidTokenException(token=refresh_token)

    async def is_valid_token(self, token: str) -> bool:
        """
        Check if provided token is still valid.
        """
        try:
            decoded_token = self._decode_token(token)
            return not self._is_token_expired(decoded_token.exp)
        except jwt.ExpiredSignatureError:
            return False
        except jwt.DecodeError:
            return False

    async def register_user(self, dto: RegisterUserDTO) -> UserDTO:
        """Register a new user."""
        hashed_password = self._get_password_hash(dto.password)
        data = asdict(dto)
        data.pop('password')
        data['hashed_password'] = hashed_password
        return await self.repo.add(AddUserDTO(**data))

    def create_token(
        self,
        payload: TokenPayload,
    ) -> str:
        """Create a new token based on the application configuration."""
        to_encode = asdict(payload)
        encoded_jwt = jwt.encode(
            to_encode,
            self._config.secret_key,
            algorithm=self._config.algorithms[0],
        )
        return encoded_jwt

    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Hash plain password and check if it equals the hashed one."""
        return self.context.verify(plain_password, hashed_password)

    def _get_password_hash(self, password: str) -> str:
        """Return hashed password according to the application crypto context."""
        return self.context.hash(password)

    def _decode_token(self, token: str) -> TokenPayload:
        """Decode token and return its payload."""
        try:
            data = jwt.decode(
                jwt=token,
                key=self._config.secret_key,
                algorithms=self._config.algorithms,
            )
            logger.info(f'Decoded token data: {data}')
            return TokenPayload(**data)
        except jwt.ExpiredSignatureError:
            raise TokenExpiredException(token)
        except jwt.DecodeError:
            raise InvalidTokenException(token)

    def _is_token_expired(self, exp_timestamp: int) -> bool:
        """Check if the token has expired."""
        current_timestamp = int(datetime.now().timestamp())
        return exp_timestamp < current_timestamp

    def __create_tokens_exp(self) -> tuple[int, int]:
        """Create expiration time in timestamp for access and refresh tokens"""
        access_token_exp = int(
            datetime.now().timestamp()
            + timedelta(minutes=self._config.access_token_expire_minutes).total_seconds()
        )
        refresh_token_exp = int(
            datetime.now().timestamp()
            + timedelta(days=self._config.refresh_token_expire_days).total_seconds()
        )

        return access_token_exp, refresh_token_exp
