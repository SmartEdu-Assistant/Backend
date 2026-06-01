from __future__ import annotations

from datetime import timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status

from app.core.config import settings
from app.core.security import (
    create_jwt_token,
    decode_jwt_token,
    verify_password,
)
from app.models import RefreshSession, User
from app.repositories import RefreshSessionRepository, UserRepository
from app.schemas import LoginRequest, TokenPair, UserCreate
from app.services.user import UserService


class AuthService:
    def __init__(
        self,
        user_repository: Annotated[UserRepository, Depends(UserRepository)],
        refresh_session_repository: Annotated[
            RefreshSessionRepository,
            Depends(RefreshSessionRepository),
        ],
        user_service: Annotated[UserService, Depends(UserService)],
    ) -> None:
        self.user_repository = user_repository
        self.refresh_session_repository = refresh_session_repository
        self.user_service = user_service

    async def register(self, payload: UserCreate) -> User:
        return await self.user_service.create(payload)

    async def login(self, payload: LoginRequest) -> tuple[User, TokenPair]:
        user = await self.user_repository.get_by_email(payload.email)
        if user is None or not verify_password(payload.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid email or password',
            )

        if user.status != 'ACTIVE':
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='User is blocked',
            )

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
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Refresh session is invalid',
            )

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
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid token subject',
            ) from exc

        user = await self.user_repository.get(user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='User not found for token',
            )
        if user.status != 'ACTIVE':
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='User is blocked',
            )
        return user

    def ensure_token_type(self, payload: dict, expected_type: str) -> None:
        if payload.get('token_type') != expected_type:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f'Invalid token type, expected {expected_type}',
            )

    def _decode_token_or_401(self, token: str) -> dict:
        try:
            return decode_jwt_token(token)
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(exc),
            ) from exc
