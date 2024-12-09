import abc
import typing as t
from dataclasses import Field as _Field


class __DataclassInstance(t.Protocol):
    __dataclass_fields__: t.ClassVar[dict[str, _Field[t.Any]]]


IT = t.TypeVar('IT', bound=__DataclassInstance)
OT = t.TypeVar('OT', bound=t.Any)


class UseCase(t.Generic[IT, OT]):
    @abc.abstractmethod
    async def __call__(self, dto: IT) -> OT: ...
