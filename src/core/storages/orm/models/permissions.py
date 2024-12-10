import typing as t

from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


permission_user_table = Table(
    'permission_user',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
    Column(
        'permission_id',
        Integer,
        ForeignKey('permissions.id', ondelete='CASCADE'),
        primary_key=True,
    ),
)


class PermissionORM(Base):
    __tablename__ = 'permissions'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    codename: Mapped[str] = mapped_column(String(30), nullable=False, index=True, unique=True)

    def to_dict(self) -> dict[str, t.Any]:
        return {'id': self.id, 'name': self.name, 'codename': self.codename}

    def __str__(self) -> str:
        return self.codename

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, other: 'PermissionORM') -> bool:
        return self.id == other.id
