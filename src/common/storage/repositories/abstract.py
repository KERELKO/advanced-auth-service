from abc import ABC, abstractmethod


class AbstractUserRepository(ABC):
    @abstractmethod
    async def get(self, id: int): ...
