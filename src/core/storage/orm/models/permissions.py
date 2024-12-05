import typing as t

from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import Mapped, mapped_column

from .common import Base

permission_user_table = Table(
    'permission_user',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('permission_id', Integer, ForeignKey('permission.id'), primary_key=True),
)


class PermissionORM(Base):
    __tablename__ = 'permission'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    codename: Mapped[str] = mapped_column(String(30), nullable=False)

    def to_dict(self) -> dict[str, t.Any]:
        return {'id': self.id, 'name': self.name, 'codename': self.codename}
