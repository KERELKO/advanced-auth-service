import typing as t

import punq  # type: ignore

from src.core import config
from src.core.config import Config
from src.core.storage.repositories.base import IPermissionRepository, IUserRepository
from src.core.storage.repositories.sqlalchemy import (
    SQLAlchemyPermissionRepository,
    SQLAlchemyUserRepository,
)
from src.core.storage.orm.db import Database
from src.modules.authentication.service import AuthenticationService


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

        container.register(AuthenticationService)

        return container

    def register(self, obj_type: type | str, *args, **kwargs):
        self.container.register(obj_type, *args, **kwargs)

    def resolve(self, obj_type: type[T] | str, *args, **kwargs) -> T:
        return t.cast(T, self.container.resolve(obj_type))

    def __contains__(self, item) -> bool:
        return bool(self.container.registrations[item])


container = Container()
