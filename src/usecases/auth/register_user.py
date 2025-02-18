from dataclasses import dataclass

from src.modules.authentication import AuthenticationService
from src.modules.authentication.dto import (
    RegisterUserDTO as _RegisterUserDTO,
)
from src.modules.authorization import AuthorizationService
from src.modules.mfa.service import MFAService
from src.core.dto.users import UserDTO

from .. import UseCase


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
