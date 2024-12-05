import typing as t
from dataclasses import Field as _Field

from src.core.exceptions import ObjectDoesNotExist


class __DataclassInstance(t.Protocol):
    __dataclass_fields__: t.ClassVar[dict[str, _Field[t.Any]]]


_T = t.TypeVar('_T', bound=__DataclassInstance)


def to_dto(cls: type[_T], data: dict[str, t.Any]) -> _T:
    """Create new instance of the `cls` with data provided in `data`"""
    return cls(**{key: value for key, value in data.items() if key in cls.__dataclass_fields__})


def raise_exc(exception: type[Exception] | Exception) -> t.NoReturn:
    raise exception


def not_found(id: int) -> t.NoReturn:
    raise ObjectDoesNotExist(id=id)
