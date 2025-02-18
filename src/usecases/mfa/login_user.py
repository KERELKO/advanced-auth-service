from dataclasses import dataclass

from src.core.dto.tokens import Token
from src.core.storages.repositories.base import IUserRepository
from src.modules.authentication import AuthenticationService
from src.modules.mfa.service import MFAService
from src.modules.mfa.dto import MFACode
from src.modules.mfa.exceptions import InvalidCodeException, MFAException

from .. import UseCase


@dataclass(eq=False, repr=False, slots=True)
class LoginUserMFA(UseCase[MFACode, tuple[Token, Token]]):
    authentication_service: AuthenticationService
    user_repository: IUserRepository
    mfa_service: MFAService

    async def __call__(self, dto: MFACode) -> tuple[Token, Token]:
        user = await self.user_repository.get(id=dto.user_id)

        if user.mfa_type != dto.mfa_type:
            raise MFAException("MFA types din't match")

        if user.mfa_type == 'code':
            if not await self.mfa_service.check_storage_code(user.id, dto.code):
                raise InvalidCodeException(dto.code)
        elif user.mfa_type == 'otp':
            if not user.mfa_secret:
                raise MFAException(
                    'User enabled MFA, but setup is incorrect: "mfa_secret" is not provided'
                )
            if not self.mfa_service.verify_mfa_code(user.mfa_secret, dto.code):
                raise InvalidCodeException(dto.code)

        return await self.authentication_service.login(user)
