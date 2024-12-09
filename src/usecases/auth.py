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
from src.modules.mfa.exceptions import InvalidCodeException

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
class LoginUser(UseCase[LoginUserDTO, tuple[Token, Token] | UserDTO]):
    authorization_service: AuthorizationService
    authentication_service: AuthenticationService
    mfa_service: MFAService

    async def __call__(self, dto: LoginUserDTO) -> tuple[Token, Token] | UserDTO:
        """Return `access` and `refresh` tokens if user logged in
        otherwise return `UserDTO` instance indicating that `MFA required`

        * if `MFA required` use `verify_mfa_code` method to verify code
        from the user's authenticator (e.g Google Authenticator)
        """
        user = await self.authentication_service.repo.get_by_username(dto.username)

        hashed_password = user.hashed_password or ''
        if self.authentication_service.verify_password(dto.password, hashed_password) is False:
            raise ApplicationException("Passwords didn't match")

        if user.mfa_enabled and user.mfa_secret:
            return user

        tokens = await self.authentication_service.login(user)
        return tokens

    async def verify_mfa_code(self, user: UserDTO, code: str) -> tuple[Token, Token]:
        if not user.mfa_secret:
            raise ApplicationException('MFA is enabled, but no MFA secret is set for this user')
        if self.mfa_service.verify_mfa_code(user.mfa_secret, code) is False:
            raise InvalidCodeException(code)

        return await self.authentication_service.login(user)
