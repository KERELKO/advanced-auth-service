import pytest
from src.core.di import Container
from src.core.dto import CreateUserDTO
from src.core.exceptions import ObjectDoesNotExist
from src.core.storage.repositories.sqlalchemy import SQLAlchemyUserRepository


@pytest.mark.asyncio
async def test_can_add_and_get_methods_of_repository(container: Container) -> None:
    repo = container.resolve(SQLAlchemyUserRepository)

    dto = CreateUserDTO(username='admin', email='admin@gmail.com', hashed_password='lalal')

    added_user = await repo.add(dto)

    assert added_user.id is not None

    assert added_user.username == dto.username

    user = await repo.get(id=added_user.id)

    assert user.hashed_password == dto.hashed_password

    with pytest.raises(ObjectDoesNotExist):
        user = await repo.get(id=-1)
