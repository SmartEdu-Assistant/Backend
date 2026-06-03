from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from sqlmodel import Field, SQLModel

from app.models.base import TimestampedModel, TimestampedPublicSchema


class EmailNotificationStatus(str, Enum):
    PENDING = 'PENDING'
    SENT = 'SENT'
    FAILED = 'FAILED'


class EmailNotificationBase(SQLModel):
    recipient: str = Field(max_length=255)
    subject: str = Field(max_length=255)
    template_name: str = Field(max_length=255)
    body: str
    status: EmailNotificationStatus = EmailNotificationStatus.PENDING
    user_id: Optional[int] = Field(default=None, foreign_key='users.id')
    sent_at: datetime | None = None
    error_message: str | None = None


class EmailNotification(EmailNotificationBase, TimestampedModel, table=True):
    __tablename__ = 'email_notifications'


class EmailNotificationCreate(EmailNotificationBase):
    pass


class EmailNotificationUpdate(SQLModel):
    status: EmailNotificationStatus | None = None
    sent_at: datetime | None = None
    error_message: str | None = None


class EmailNotificationPublic(EmailNotificationBase, TimestampedPublicSchema):
    pass
