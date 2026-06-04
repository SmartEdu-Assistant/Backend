from __future__ import annotations

from datetime import datetime, timedelta
from typing import Annotated

from fastapi import BackgroundTasks, Depends

from app.core.config import settings
from app.core.exceptions import AuthenticationError, AuthorizationError
from app.core.security import (
    create_jwt_token,
    decode_jwt_token,
    get_password_hash,
    verify_password,
)
from app.models import RefreshSession, User
from app.repositories import EmailNotificationRepository, RefreshSessionRepository, UserRepository
from app.schemas import (
    ChangePasswordRequest,
    ConfirmAccountRequest,
    LoginRequest,
    TokenPair,
    UserCreate,
)
from app.services.email_notification import EmailNotificationService
from app.services.user import UserService


class AuthService:
    def __init__(
        self,
        user_repository: Annotated[UserRepository, Depends(UserRepository)],
        refresh_session_repository: Annotated[
            RefreshSessionRepository,
            Depends(RefreshSessionRepository),
        ],
        email_notification_repository: Annotated[
            EmailNotificationRepository,
            Depends(EmailNotificationRepository),
        ],
        email_notification_service: Annotated[
            EmailNotificationService,
            Depends(EmailNotificationService),
        ],
        user_service: Annotated[UserService, Depends(UserService)],
    ) -> None:
        self.user_repository = user_repository
        self.refresh_session_repository = refresh_session_repository
        self.email_notification_repository = email_notification_repository
        self.email_notification_service = email_notification_service
        self.user_service = user_service

    async def register(
        self,
        payload: UserCreate,
        background_tasks: BackgroundTasks,
    ) -> User:
        user = await self.user_service.create(payload)
        notification = await self.email_notification_service.queue_account_confirmation(user)
        background_tasks.add_task(
            self.email_notification_service.send_notification,
            notification.id,
        )
        return user

    async def login(self, payload: LoginRequest) -> tuple[User, TokenPair]:
        user = await self.user_repository.get_by_email(payload.email)
        if user is None or not verify_password(payload.password, user.password_hash):
            raise AuthenticationError('Invalid email or password')

        if user.status != 'ACTIVE':
            raise AuthorizationError('User is blocked')

        if settings.auth.require_verified_account and not user.is_verified:
            raise AuthorizationError('Account is not confirmed yet')

        token_pair = await self._issue_token_pair(user)
        return user, token_pair

    async def refresh(self, refresh_token: str) -> tuple[User, TokenPair]:
        payload = self._decode_token_or_401(refresh_token)
        self.ensure_token_type(payload, 'refresh')
        user = await self._get_user_from_payload(payload)
        refresh_session = await self.refresh_session_repository.get_active_by_jti(
            payload['jti'],
        )
        if refresh_session is None or refresh_session.user_id != user.id:
            raise AuthenticationError('Refresh session is invalid')

        await self.refresh_session_repository.revoke(refresh_session)
        token_pair = await self._issue_token_pair(user)
        return user, token_pair

    async def logout(self, refresh_token: str) -> None:
        payload = self._decode_token_or_401(refresh_token)
        self.ensure_token_type(payload, 'refresh')
        user = await self._get_user_from_payload(payload)
        await self.refresh_session_repository.revoke_for_user(user.id)

    async def get_user_by_access_token(self, access_token: str) -> User:
        payload = self._decode_token_or_401(access_token)
        self.ensure_token_type(payload, 'access')
        return await self._get_user_from_payload(payload)

    async def confirm_account(self, payload: ConfirmAccountRequest) -> User:
        notification = await self.email_notification_repository.get_by_confirmation_token(
            payload.token,
        )
        if notification is None or notification.confirmation_token_expires_at is None:
            raise AuthenticationError('Verification token is invalid')
        if notification.confirmation_token_expires_at < datetime.utcnow():
            raise AuthenticationError('Verification token has expired')
        if notification.user_id is None:
            raise AuthenticationError('Verification token is invalid')

        user = await self.user_repository.get(notification.user_id)
        if user is None:
            raise AuthenticationError('User not found for verification token')

        if not user.is_verified:
            user = await self.user_repository.update(
                user,
                {
                    'is_verified': True,
                },
            )

        await self.email_notification_repository.update(
            notification,
            {
                'confirmation_token': None,
                'confirmation_token_expires_at': None,
            },
        )
        return user

    async def change_password(
        self,
        current_user: User,
        payload: ChangePasswordRequest,
        background_tasks: BackgroundTasks,
    ) -> None:
        if not verify_password(payload.current_password, current_user.password_hash):
            raise AuthenticationError('Current password is invalid')

        await self.user_repository.update(
            current_user,
            {'password_hash': get_password_hash(payload.new_password)},
        )
        await self.refresh_session_repository.revoke_for_user(current_user.id)

        notification = await self.email_notification_service.queue_password_changed(
            current_user,
        )
        background_tasks.add_task(
            self.email_notification_service.send_notification,
            notification.id,
        )

    async def _issue_token_pair(self, user: User) -> TokenPair:
        subject = str(user.id)
        access_token, _, _ = create_jwt_token(
            subject=subject,
            expires_delta=timedelta(minutes=settings.auth.access_token_ttl_minutes),
            token_type='access',
        )
        refresh_token, refresh_jti, refresh_expires_at = create_jwt_token(
            subject=subject,
            expires_delta=timedelta(days=settings.auth.refresh_token_ttl_days),
            token_type='refresh',
        )

        refresh_session = RefreshSession(
            user_id=user.id,
            jti=refresh_jti,
            expires_at=refresh_expires_at,
        )
        await self.refresh_session_repository.save(refresh_session)

        return TokenPair(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    async def _get_user_from_payload(self, payload: dict) -> User:
        try:
            user_id = int(payload['sub'])
        except (TypeError, ValueError) as exc:
            raise AuthenticationError('Invalid token subject') from exc

        user = await self.user_repository.get(user_id)
        if user is None:
            raise AuthenticationError('User not found for token')
        if user.status != 'ACTIVE':
            raise AuthorizationError('User is blocked')
        return user

    def ensure_token_type(self, payload: dict, expected_type: str) -> None:
        if payload.get('token_type') != expected_type:
            raise AuthenticationError(
                f'Invalid token type, expected {expected_type}',
            )

    def _decode_token_or_401(self, token: str) -> dict:
        try:
            return decode_jwt_token(token)
        except ValueError as exc:
            raise AuthenticationError(str(exc)) from exc
