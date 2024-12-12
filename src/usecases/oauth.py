# fmt: off
from dataclasses import dataclass

from src.core.di import (
    container,
    Container,
)
from src.core.dto.tokens import Token
from src.core.dto.users import (
    ExternalUser,
    UserDTO,
)
from src.core.exceptions import ApplicationException
from src.core.services.interfaces import AbstractOAuthService
from src.core.storages.repositories.base import IUserRepository
from src.modules.authentication.service import AuthenticationService
from src.modules.authorization.service import AuthorizationService
from src.modules.oauth.dto import OAuthCode
from src.modules.oauth.service import (
    GitHubOAuthService,
    GoogleOAuthService,
)

from . import UseCase


def _get_service_by_provider(provider: str, container: Container) -> AbstractOAuthService:
    if provider == 'google':
        return container.resolve(GoogleOAuthService)
    elif provider == 'github':
        return container.resolve(GitHubOAuthService)
    raise ApplicationException(f'Unsupported provider: {provider}')


@dataclass(eq=False, repr=False, slots=True)
class OAuthRegisterUser(UseCase[OAuthCode, UserDTO]):
    authorization_service: AuthorizationService
    user_repository: IUserRepository

    async def __call__(self, dto: OAuthCode) -> UserDTO:
        service: AbstractOAuthService = _get_service_by_provider(dto.provider, container)

        user: ExternalUser = await service.get_user(code=dto.code)
        add_user_dto = user.as_add_user_dto()
        add_user_dto.permissions = self.authorization_service.default_permission_set

        registered_user = await self.user_repository.add(add_user_dto)
        return registered_user


class OAuthLogin(UseCase[OAuthCode, tuple[Token, Token]]):
    authentication_service: AuthenticationService
    user_repository: IUserRepository

    async def __call__(self, dto: OAuthCode) -> tuple[Token, Token]:
        service: AbstractOAuthService = _get_service_by_provider(dto.provider, container)

        external_user: ExternalUser = await service.get_user(code=dto.code)

        user = await self.user_repository.get_by_oauth_provider(external_user.id, dto.provider)

        return await self.authentication_service.login(user)
