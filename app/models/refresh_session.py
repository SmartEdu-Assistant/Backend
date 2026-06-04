from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from app.models.base import TimestampedModel

if TYPE_CHECKING:
    from app.models.user import User


class RefreshSession(TimestampedModel, table=True):
    __tablename__ = 'refresh_sessions'

    user_id: int = Field(foreign_key='users.id', nullable=False, index=True)
    jti: str = Field(unique=True, index=True, max_length=255)
    expires_at: datetime
    revoked_at: datetime | None = None

    user: 'User' = Relationship()
