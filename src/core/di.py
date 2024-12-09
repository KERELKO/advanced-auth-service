import typing as t

import punq

from src.core import config
from src.core.config import Config
from src.core.storage.repositories.base import IPermissionRepository, IUserRepository
from src.core.storage.repositories.sqlalchemy import (
    SQLAlchemyPermissionRepository,
    SQLAlchemyUserRepository,
)
from src.core.storage.orm.db import Database
from src.modules.authentication.service import AuthenticationService
from src.modules.authorization.service import AuthorizationService
from src.modules.mfa.service import MFAService
from src.usecases.auth import LoginUser, RegisterUser


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
        container.register(IUserRepository, SQLAlchemyUserRepository, scope=punq.Scope.singleton)
        container.register(
            IPermissionRepository,
            SQLAlchemyPermissionRepository,
            scope=punq.Scope.singleton,
        )

        container.register(AuthenticationService, scope=punq.Scope.singleton)
        container.register(AuthorizationService, scope=punq.Scope.singleton)
        container.register(MFAService, instance=MFAService(), scope=punq.Scope.singleton)

        container.register(RegisterUser)
        container.register(LoginUser)

        return container

    def register(self, obj_type: type | str, *args, **kwargs):
        self.container.register(obj_type, *args, **kwargs)

    def resolve(self, obj_type: type[T] | str, *args, **kwargs) -> T:
        return t.cast(T, self.container.resolve(obj_type))

    def __contains__(self, item) -> bool:
        return bool(self.container.registrations[item])


container = Container()
