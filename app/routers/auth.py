from datetime import timedelta
from urllib.parse import parse_qs
from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Cookie, Request, Response, Security, status
from pydantic import ValidationError

from app.core.api_docs import (
    AUTH_ERROR_RESPONSES,
    BAD_REQUEST_ERROR_RESPONSES,
    CONFLICT_ERROR_RESPONSES,
    SERVER_ERROR_RESPONSES,
    VALIDATION_ERROR_RESPONSES,
    combine_responses,
)
from app.core.config import settings
from app.core.exceptions import DomainValidationError
from app.dependencies.auth import get_current_user
from app.dependencies.services import AuthServiceDep
from app.models import User
from app.schemas import (
    AuthSuccessResponse,
    ChangePasswordRequest,
    ConfirmAccountRequest,
    LoginRequest,
    TokenPair,
    UserCreate,
    UserPublic,
)


router = APIRouter(
    prefix='/auth',
    tags=['auth'],
    responses=combine_responses(SERVER_ERROR_RESPONSES, VALIDATION_ERROR_RESPONSES),
)


def _set_refresh_cookie(response: Response, refresh_token: str) -> None:
    response.set_cookie(
        key=settings.auth.refresh_cookie_name,
        value=refresh_token,
        httponly=True,
        secure=settings.auth.refresh_cookie_secure,
        samesite=settings.auth.refresh_cookie_samesite,
        domain=settings.auth.refresh_cookie_domain,
        path=settings.auth.refresh_cookie_path,
        max_age=int(
            timedelta(days=settings.auth.refresh_token_ttl_days).total_seconds(),
        ),
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
    responses=combine_responses(
        BAD_REQUEST_ERROR_RESPONSES,
        CONFLICT_ERROR_RESPONSES,
    ),
)
async def register(
    payload: UserCreate,
    background_tasks: BackgroundTasks,
    service: AuthServiceDep,
):
    await service.register(payload, background_tasks)
    return AuthSuccessResponse(
        message='Registration completed. Please confirm your account by email.',
    )


async def _parse_login_request(request: Request) -> LoginRequest:
    content_type = request.headers.get('content-type', '').split(';', maxsplit=1)[0]

    try:
        if content_type == 'application/json':
            payload = await request.json()
            return LoginRequest.model_validate(payload)

        if content_type == 'application/x-www-form-urlencoded':
            form_data = parse_qs((await request.body()).decode('utf-8'))
            username = form_data.get('username', [None])[0]
            password = form_data.get('password', [None])[0]
            return LoginRequest.model_validate(
                {
                    'email': username,
                    'password': password,
                },
            )
    except (ValueError, ValidationError) as exc:
        raise DomainValidationError('Invalid login payload') from exc

    raise DomainValidationError(
        'Unsupported content type for login. Use application/json or application/x-www-form-urlencoded.',
    )


@router.post(
    '/login',
    response_model=TokenPair,
    responses=AUTH_ERROR_RESPONSES,
)
async def login(
    request: Request,
    response: Response,
    service: AuthServiceDep,
):
    payload = await _parse_login_request(request)
    _, token_pair = await service.login(payload)
    _set_refresh_cookie(response, token_pair.refresh_token)
    return token_pair


@router.get('/me', response_model=UserPublic, responses=AUTH_ERROR_RESPONSES)
async def me(
    current_user: Annotated[User, Security(get_current_user, scopes=['profile:read'])],
):
    return current_user


@router.post('/logout', response_model=AuthSuccessResponse, responses=AUTH_ERROR_RESPONSES)
async def logout(
    response: Response,
    service: AuthServiceDep,
    refresh_token: Annotated[str | None, Cookie(alias=settings.auth.refresh_cookie_name)] = None,
):
    if refresh_token:
        await service.logout(refresh_token)
    _delete_refresh_cookie(response)
    return AuthSuccessResponse(message='Logout completed successfully.')


@router.post('/refresh', response_model=TokenPair, responses=AUTH_ERROR_RESPONSES)
async def refresh(
    response: Response,
    service: AuthServiceDep,
    refresh_token: Annotated[str, Cookie(alias=settings.auth.refresh_cookie_name)],
):
    _, token_pair = await service.refresh(refresh_token)
    _set_refresh_cookie(response, token_pair.refresh_token)
    return token_pair


@router.post(
    '/confirm-account',
    response_model=AuthSuccessResponse,
    responses=AUTH_ERROR_RESPONSES,
)
async def confirm_account(
    payload: ConfirmAccountRequest,
    service: AuthServiceDep,
):
    await service.confirm_account(payload)
    return AuthSuccessResponse(message='Account confirmed successfully.')


@router.post(
    '/change-password',
    response_model=AuthSuccessResponse,
    responses=combine_responses(AUTH_ERROR_RESPONSES, BAD_REQUEST_ERROR_RESPONSES),
)
async def change_password(
    payload: ChangePasswordRequest,
    background_tasks: BackgroundTasks,
    service: AuthServiceDep,
    current_user: Annotated[User, Security(get_current_user, scopes=['profile:read'])],
):
    await service.change_password(current_user, payload, background_tasks)
    return AuthSuccessResponse(message='Password changed successfully.')
