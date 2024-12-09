from dataclasses import dataclass

from src.core.dto.tokens import Token
from src.core.dto.users import UserDTO
from src.core.exceptions import ApplicationException
from src.modules.authentication import AuthenticationService
from src.modules.authentication.dto import (
    LoginUserDTO,
    RegisterUserDTO,
)
from src.modules.authorization import AuthorizationService
from src.modules.mfa import MFAService
from src.modules.mfa.dto import Code

from . import UseCase


@dataclass(eq=False, repr=False, slots=True)
class RegisterUser(UseCase[RegisterUserDTO, UserDTO]):
    authentication_service: AuthenticationService
    authorization_service: AuthorizationService
    mfa_service: MFAService

    async def __call__(self, dto: RegisterUserDTO) -> UserDTO:
        mfa_secret = self.mfa_service.generate_secret()
        user_permissions = dto.permissions or self.authorization_service.default_permission_set

        dto.permissions = user_permissions
        dto.mfa_secret = mfa_secret
        new_user = await self.authentication_service.register_user(dto)

        return new_user


@dataclass(eq=False, repr=False, slots=True)
class LoginUser(UseCase[LoginUserDTO, tuple[Token, Token] | Code]):
    authorization_service: AuthorizationService
    authentication_service: AuthenticationService
    mfa_service: MFAService

    async def __call__(self, dto: LoginUserDTO) -> tuple[Token, Token] | Code:
        user = await self.authentication_service.repo.get_by_username(dto.username)

        if (
            self.authentication_service.verify_password(
                dto.password,
                user.hashed_password or '',
            )
            is False
        ):
            raise ApplicationException("Passwords didn't match")

        if user.mfa_enabled and user.mfa_secret:
            return self.mfa_service.generate_one_time_password(user.mfa_secret)

        tokens = await self.authentication_service.login(user)
        return tokens


@dataclass(eq=False, repr=False, slots=True)
class LoginUserWithCode(UseCase[Code, tuple[Token, Token]]):
    authorization_service: AuthorizationService
    authentication_service: AuthenticationService
    mfa_service: MFAService

    async def __call__(self, code: Code) -> tuple[Token, Token]: ...
