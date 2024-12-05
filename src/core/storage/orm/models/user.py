from typing import Any

import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .common import Base
from .permissions import RoleORM


class UserORM(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30))
    email: Mapped[str | None] = mapped_column(String(40), nullable=True)
    hashed_password: Mapped[str | None] = mapped_column(String(200), nullable=True)
    mfa_enabled: Mapped[bool] = mapped_column(Boolean(), default=False, nullable=False)
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
    )

    role_id: Mapped[int | None] = mapped_column(ForeignKey('role.id'), nullable=True)
    role: Mapped[RoleORM] = relationship(back_populates='users')

    def __str__(self) -> str:
        return self.username

    def to_dict(self) -> dict[str, Any]:
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role_id': self.role_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'hashed_password': self.hashed_password,
            'mfa_enabled': self.mfa_enabled,
            'mfa_secret': self.mfa_secret,
            'oauth_provider': self.oauth_provider,
            'oauth_provider_id': self.oauth_provider_id,
        }
