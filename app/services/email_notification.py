from __future__ import annotations

from datetime import datetime
from pathlib import Path
from string import Template

from fastapi import Depends
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType

from app.core.config import settings
from app.core.logging import logger
from app.db import AsyncSessionFactory
from app.models import (
    EmailNotificationCreate,
    EmailNotificationStatus,
    User,
)
from app.repositories import EmailNotificationRepository


class EmailNotificationService:
    def __init__(
        self,
        repository: EmailNotificationRepository = Depends(EmailNotificationRepository),
    ) -> None:
        self.repository = repository
        self.templates_dir = Path(settings.email.templates_dir)

    async def queue_account_confirmation(self, user: User):
        confirmation_url = (
            f'{settings.email.frontend_base_url}/confirm-account?token={user.verification_token}'
        )
        body = self._render_template(
            'confirm_account.html',
            {
                'first_name': user.first_name,
                'confirmation_url': confirmation_url,
            },
        )
        return await self.repository.create(
            EmailNotificationCreate(
                recipient=user.email,
                subject='Confirm your SmartEdu account',
                template_name='confirm_account.html',
                body=body,
                user_id=user.id,
            ).model_dump(exclude_none=True),
        )

    async def queue_password_changed(self, user: User):
        body = self._render_template(
            'password_changed.html',
            {
                'first_name': user.first_name,
                'support_email': settings.smtp.from_email,
            },
        )
        return await self.repository.create(
            EmailNotificationCreate(
                recipient=user.email,
                subject='Your SmartEdu password has been changed',
                template_name='password_changed.html',
                body=body,
                user_id=user.id,
            ).model_dump(exclude_none=True),
        )

    async def send_notification(self, notification_id: int) -> None:
        async with AsyncSessionFactory() as session:
            repository = EmailNotificationRepository(session)
            notification = await repository.get(notification_id)
            if notification is None:
                logger.warning('Email notification %s was not found', notification_id)
                return

            try:
                if not settings.smtp.enabled:
                    raise RuntimeError('SMTP sending is disabled in settings')

                message = MessageSchema(
                    subject=notification.subject,
                    recipients=[notification.recipient],
                    body=notification.body,
                    subtype=MessageType.html,
                )
                await FastMail(self._connection_config()).send_message(message)
                await repository.update(
                    notification,
                    {
                        'status': EmailNotificationStatus.SENT,
                        'sent_at': datetime.utcnow(),
                        'error_message': None,
                    },
                )
            except Exception as exc:
                logger.exception(
                    'Failed to send email notification %s',
                    notification_id,
                    exc_info=exc,
                )
                await repository.update(
                    notification,
                    {
                        'status': EmailNotificationStatus.FAILED,
                        'error_message': str(exc),
                    },
                )

    def _render_template(self, template_name: str, context: dict[str, str]) -> str:
        template_path = self.templates_dir / template_name
        content = template_path.read_text(encoding='utf-8')
        return Template(content).safe_substitute(context)

    @staticmethod
    def _connection_config() -> ConnectionConfig:
        return ConnectionConfig(
            MAIL_USERNAME=settings.smtp.username,
            MAIL_PASSWORD=settings.smtp.password,
            MAIL_FROM=settings.smtp.from_email,
            MAIL_FROM_NAME=settings.smtp.from_name,
            MAIL_PORT=settings.smtp.port,
            MAIL_SERVER=settings.smtp.host,
            MAIL_STARTTLS=settings.smtp.starttls,
            MAIL_SSL_TLS=settings.smtp.ssl_tls,
            USE_CREDENTIALS=True,
            VALIDATE_CERTS=settings.smtp.validate_certs,
        )
