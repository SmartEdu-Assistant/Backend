from typing import Annotated

from fastapi import APIRouter, Cookie, Response, Security, status

from app.core.config import settings
from app.dependencies.auth import get_current_user
from app.dependencies.services import AuthServiceDep
from app.models import User
from app.schemas import (
    AuthSuccessResponse,
    LoginRequest,
    TokenPair,
    UserCreate,
    UserPublic,
)


router = APIRouter(prefix='/auth', tags=['auth'])


def _set_refresh_cookie(response: Response, refresh_token: str) -> None:
    response.set_cookie(
        key=settings.auth.refresh_cookie_name,
        value=refresh_token,
        httponly=True,
        secure=settings.auth.refresh_cookie_secure,
        samesite=settings.auth.refresh_cookie_samesite,
        domain=settings.auth.refresh_cookie_domain,
        path=settings.auth.refresh_cookie_path,
        max_age=settings.auth.refresh_token_ttl_days * 24 * 60 * 60,
    )


def _delete_refresh_cookie(response: Response) -> None:
    response.delete_cookie(
        key=settings.auth.refresh_cookie_name,
        domain=settings.auth.refresh_cookie_domain,
        path=settings.auth.refresh_cookie_path,
    )


@router.post(
    '/register',
    response_model=AuthSuccessResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    payload: UserCreate,
    service: AuthServiceDep,
):
    await service.register(payload)
    return AuthSuccessResponse()


@router.post('/login', response_model=TokenPair)
async def login(
    payload: LoginRequest,
    response: Response,
    service: AuthServiceDep,
):
    _, token_pair = await service.login(payload)
    _set_refresh_cookie(response, token_pair.refresh_token)
    return token_pair


@router.get('/me', response_model=UserPublic)
async def me(
    current_user: Annotated[User, Security(get_current_user, scopes=['profile:read'])],
):
    return current_user


@router.post('/logout', response_model=AuthSuccessResponse)
async def logout(
    response: Response,
    service: AuthServiceDep,
    refresh_token: Annotated[str | None, Cookie(alias=settings.auth.refresh_cookie_name)] = None,
):
    if refresh_token:
        await service.logout(refresh_token)
    _delete_refresh_cookie(response)
    return AuthSuccessResponse()


@router.post('/refresh', response_model=TokenPair)
async def refresh(
    response: Response,
    service: AuthServiceDep,
    refresh_token: Annotated[str, Cookie(alias=settings.auth.refresh_cookie_name)],
):
    _, token_pair = await service.refresh(refresh_token)
    _set_refresh_cookie(response, token_pair.refresh_token)
    return token_pair
