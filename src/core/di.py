import typing as t

import punq

from src.core.config import (
    Config,
    config,
)
from src.core.services.interfaces import AbstractNotificationService
from src.core.services.notifications import EmailNotificationService
from src.core.storages.db import Database
from src.core.storages.repositories.base import (
    AbstractCodeRepository,
    IPermissionRepository,
    IUserRepository,
)
from src.core.storages.repositories.redis import RedisCodeRepository
from src.core.storages.repositories.sqlalchemy import (
    SQLAlchemyPermissionRepository,
    SQLAlchemyUserRepository,
)
from src.modules.authentication.service import AuthenticationService
from src.modules.authorization.service import AuthorizationService
from src.modules.mfa.service import MFAService
from src.modules.oauth.service import GitHubOAuthService, GoogleOAuthService
from src.usecases.auth.login_user import LoginUser
from src.usecases.auth.register_user import RegisterUser

from src.usecases.mfa.login_user import LoginUserMFA
from src.usecases.mfa.send_code import SendMFACode
from src.usecases.mfa.setup import SetupUserMFA

from src.usecases.oauth.login_user import OAuthLogin


T = t.TypeVar('T')


class Container:
    def __init__(self, instance: punq.Container | None = None) -> None:
        self.container = instance or self._init_container()

    @staticmethod
    def _init_container() -> punq.Container:
        container = punq.Container()

        container.register(Config, instance=config, scope=punq.Scope.singleton)
        db = Database(config)
        container.register(Database, instance=db)
        container.register(IUserRepository, lambda: SQLAlchemyUserRepository(db.session_factory()))
        container.register(
            IPermissionRepository,
            lambda: SQLAlchemyPermissionRepository(db.session_factory()),
        )
        code_repo = RedisCodeRepository(config)
        container.register(AbstractCodeRepository, instance=code_repo, scope=punq.Scope.singleton)

        container.register(EmailNotificationService, scope=punq.Scope.singleton)
        container.register(
            AbstractNotificationService,
            EmailNotificationService,
            scope=punq.Scope.singleton,
        )
        container.register(AuthenticationService, scope=punq.Scope.singleton)
        container.register(AuthorizationService, scope=punq.Scope.singleton)
        container.register(MFAService, instance=MFAService(code_repo), scope=punq.Scope.singleton)
        container.register(GoogleOAuthService)
        container.register(GitHubOAuthService)

        container.register(RegisterUser)
        container.register(LoginUser)
        container.register(SetupUserMFA)
        container.register(LoginUserMFA)
        container.register(SendMFACode)
        container.register(OAuthLogin)

        return container

    def register(self, obj_type: type | str, *args, **kwargs):
        self.container.register(obj_type, *args, **kwargs)

    def resolve(self, obj_type: type[T] | str, *args, **kwargs) -> T:
        return t.cast(T, self.container.resolve(obj_type))

    def __contains__(self, item) -> bool:
        return bool(self.container.registrations[item])


container = Container()
