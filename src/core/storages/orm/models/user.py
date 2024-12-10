import typing as t

import datetime

from sqlalchemy import Boolean, DateTime, String, func, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.dto.permissions import PermissionDTO
from src.core.utils import to_dto

from .base import Base
from .permissions import PermissionORM, permission_user_table


class UserORM(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30), nullable=False, unique=True, index=True)
    email: Mapped[str | None] = mapped_column(String(40), nullable=True)
    hashed_password: Mapped[str | None] = mapped_column(String(200), nullable=True)
    mfa_enabled: Mapped[bool] = mapped_column(
        Boolean(), default=False, nullable=False, server_default=text('false')
    )
    mfa_secret: Mapped[str] = mapped_column(String(), nullable=True)
    oauth_provider: Mapped[str | None] = mapped_column(String(30), nullable=True)
    oauth_provider_id: Mapped[str | None] = mapped_column(String(), nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        onupdate=func.now(),
        default=datetime.datetime.now,
        server_default=func.now(),
    )

    permissions: Mapped[list[PermissionORM]] = relationship(
        secondary=permission_user_table,
        lazy='noload',
        backref='users',
        passive_deletes=True,
    )

    def __str__(self) -> str:
        return self.username

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, other: 'PermissionORM') -> bool:
        return self.id == other.id

    def to_dict(self) -> dict[str, t.Any]:
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'hashed_password': self.hashed_password,
            'mfa_enabled': self.mfa_enabled,
            'mfa_secret': self.mfa_secret,
            'oauth_provider': self.oauth_provider,
            'oauth_provider_id': self.oauth_provider_id,
            'permissions': [
                to_dto(PermissionDTO, permission.to_dict()) for permission in self.permissions
            ],
        }
