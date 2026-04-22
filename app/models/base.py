from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from sqlmodel import Field, SQLModel


class BaseTableModel(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)


class TimestampedModel(BaseTableModel):
    created_at: datetime = Field(
        default_factory=datetime.utcnow, nullable=False
    )


class UserRole(str, Enum):
    ADMIN = 'ADMIN'
    TEACHER = 'TEACHER'


class UserStatus(str, Enum):
    ACTIVE = 'ACTIVE'
    BLOCKED = 'BLOCKED'
