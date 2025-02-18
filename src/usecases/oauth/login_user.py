# fmt: off
from dataclasses import dataclass

from src.core.dto.tokens import Token
from src.core.dto.users import ExternalUser
from src.core.exceptions import (
    ApplicationException,
    ObjectDoesNotExist,
)
from src.core.services.interfaces import AbstractOAuthService
from src.core.storages.repositories.base import IUserRepository
from src.modules.authentication.service import AuthenticationService
from src.modules.authorization.service import AuthorizationService
from src.modules.oauth.dto import OAuthCode
from src.modules.oauth.service import (
    GitHubOAuthService,
    GoogleOAuthService,
)

from .. import UseCase


def _get_service_by_provider(provider: str) -> AbstractOAuthService:
    from src.core.di import container

    if provider == 'google':
        return container.resolve(GoogleOAuthService)
    elif provider == 'github':
        return container.resolve(GitHubOAuthService)
    raise ApplicationException(f'Unsupported provider: {provider}')


@dataclass(eq=False, repr=False, slots=True)
class OAuthLogin(UseCase[OAuthCode, tuple[Token, Token]]):
    authentication_service: AuthenticationService
    authorization_service: AuthorizationService
    user_repository: IUserRepository

    async def __call__(self, dto: OAuthCode) -> tuple[Token, Token]:
        service: AbstractOAuthService = _get_service_by_provider(dto.provider)

        external_user: ExternalUser = await service.get_user(code=dto.code)
        try:
            user = await self.user_repository.get_by_oauth_provider(external_user.id, dto.provider)
        except ObjectDoesNotExist:
            add_user_dto = external_user.as_add_user_dto()
            add_user_dto.permissions = self.authorization_service.default_permission_set

            user = await self.user_repository.add(add_user_dto)

        return await self.authentication_service.login(user)
