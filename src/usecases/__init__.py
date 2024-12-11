import abc
import typing as t

IT = t.TypeVar('IT', bound=t.Any)
OT = t.TypeVar('OT', bound=t.Any)


class UseCase(t.Generic[IT, OT]):
    @abc.abstractmethod
    async def __call__(self, dto: IT) -> OT: ...
