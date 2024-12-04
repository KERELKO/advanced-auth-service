import typing as t

from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .common import Base

if t.TYPE_CHECKING:
    from .user import UserORM

role_permission_table = Table(
    'role_permission',
    Base.metadata,
    Column('role_id', Integer, ForeignKey('role.id'), primary_key=True),
    Column('permission_id', Integer, ForeignKey('permission.id'), primary_key=True),
)


class PermissionORM(Base):
    __tablename__ = 'permission'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    value: Mapped[int | None] = mapped_column(nullable=True)

    roles: Mapped[list['RoleORM']] = relationship(
        secondary=role_permission_table,
        back_populates='permissions',
    )


class RoleORM(Base):
    __tablename__ = 'role'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)

    users: Mapped[list['UserORM']] = relationship(back_populates='role')

    permissions: Mapped[list['PermissionORM']] = relationship(
        secondary=role_permission_table,
        back_populates='roles',
    )
