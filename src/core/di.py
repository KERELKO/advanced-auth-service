import typing as t

import rodi

from src.core.storage.repositories.abstract import AbstractUserRepository
from src.core.storage.repositories.sqlalchemy import SQLAlchemyUserRepository


T = t.TypeVar('T')


class Container:
    def __init__(self) -> None:
        self.container = self._init_container()

    @staticmethod
    def _init_container() -> rodi.Container:
        container = rodi.Container()

        container.register(AbstractUserRepository, SQLAlchemyUserRepository)

        return container

    def register(self, obj_type: type | str, *args, **kwargs):
        self.container.register(obj_type, *args, **kwargs)

    def resolve(self, obj_type: type[T] | str, *args, **kwargs) -> T:
        return self.container.resolve(obj_type, *args, **kwargs)

    def __contains__(self, item) -> bool:
        return item in self.container
