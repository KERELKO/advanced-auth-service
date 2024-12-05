from dataclasses import dataclass


@dataclass(eq=False, repr=False)
class CreatePermissionDTO:
    name: str
    codename: str


@dataclass(eq=False, repr=False)
class PermissionDTO:
    id: int
    name: str
    codename: str
