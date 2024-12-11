from dataclasses import dataclass

from src.core.dto.tokens import Token
from src.core.dto.users import UserDTO
from src.core.exceptions import ApplicationException
from src.modules.authentication import AuthenticationService
from src.modules.authentication.dto import (
    LoginUserDTO as _LoginUserDTO,
    RegisterUserDTO as _RegisterUserDTO,
)
from src.modules.authorization import AuthorizationService
from src.modules.mfa.service import MFAService
from src.modules.mfa.dto import MFARequired
from src.modules.mfa.exceptions import InvalidSecretKeyException

from . import UseCase


@dataclass(eq=False, repr=False, slots=True)
class RegisterUser(UseCase[_RegisterUserDTO, UserDTO]):
    authentication_service: AuthenticationService
    authorization_service: AuthorizationService
    mfa_service: MFAService

    async def __call__(self, dto: _RegisterUserDTO) -> UserDTO:
        mfa_secret = self.mfa_service.generate_secret()
        user_permissions = dto.permissions or self.authorization_service.default_permission_set

        dto.permissions = user_permissions
        dto.mfa_secret = mfa_secret
        new_user = await self.authentication_service.register_user(dto)

        return new_user


@dataclass(eq=False, repr=False, slots=True)
class LoginUser(UseCase[_LoginUserDTO, tuple[Token, Token] | MFARequired]):
    authorization_service: AuthorizationService
    authentication_service: AuthenticationService
    mfa_service: MFAService

    async def __call__(self, dto: _LoginUserDTO) -> tuple[Token, Token] | MFARequired:
        """Return `access` and `refresh` tokens if user logged in
        otherwise return `MFARequired` instance indicating that `MFA required`
        """
        user = await self.authentication_service.repo.get_by_username(dto.username)

        hashed_password = user.hashed_password or ''
        if self.authentication_service.verify_password(dto.password, hashed_password) is False:
            raise ApplicationException("Passwords didn't match")

        if user.mfa_enabled and not user.mfa_secret:
            raise InvalidSecretKeyException(user.mfa_secret)
        elif user.mfa_enabled and user.mfa_secret:
            if not user.mfa_type:
                raise ApplicationException(
                    'User enabled MFA, but setup is incorrect: "mfa_type" is not provided'
                )
            return MFARequired(user=user, mfa_type=user.mfa_type)

        tokens = await self.authentication_service.login(user)
        return tokens
