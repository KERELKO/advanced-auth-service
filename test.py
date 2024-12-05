import asyncio

from src.core.dto import CreateUserDTO, UserDTO
from src.core.di import container, AbstractUserRepository

repo = container.resolve(AbstractUserRepository)


async def add(dto: CreateUserDTO):
    new_user = await repo.add(dto)

    return new_user


async def get(id: int) -> UserDTO:
    return await repo.get(id=id)


async def main():
    u = CreateUserDTO(username='admin')
    print(1)
    new_u = await repo.add(u)
    g = await repo.get(new_u.id)
    print(g.username)


asyncio.run(main())
