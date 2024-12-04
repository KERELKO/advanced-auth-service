import typing as t
from dataclasses import dataclass, field

DT = t.TypeVar('DT')


@dataclass(eq=False, repr=False)
class APIResponse(t.Generic[DT]):
    data: DT
    meta: dict[str, t.Any] = field(default_factory=dict)
