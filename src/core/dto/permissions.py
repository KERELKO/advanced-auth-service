from dataclasses import dataclass


@dataclass(eq=False, repr=False, slots=True)
class AddPermissionDTO:
    name: str
    codename: str


@dataclass(slots=True)
class PermissionDTO:
    id: int
    name: str
    codename: str
