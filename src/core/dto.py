from dataclasses import dataclass


@dataclass(eq=False, repr=False, slots=True)
class UserDTO:
    id: int
    username: str
    email: str | None = None
    phone: str | None = None


@dataclass(eq=False, repr=False, slots=True)
class UpdateUserDTO:
    username: str | None = None
    email: str | None = None
    phone: str | None = None
