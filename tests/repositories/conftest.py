import punq
import pytest

from src.core import config
from src.core.config import Config
from src.core.di import Container
from src.core.storage.orm.config import Database
from src.core.storage.repositories.sqlalchemy import SQLAlchemyUserRepository


@pytest.fixture
def container() -> Container:
    cont = Container()

    cont.register(Config, instance=config, scope=punq.Scope.singleton)
    db = Database(config)
    cont.register(Database, instance=db)
    cont.register(
        SQLAlchemyUserRepository,
        instance=(SQLAlchemyUserRepository(db.async_session_factory)),
    )

    return cont
