from fastapi import APIRouter, Security, status

from app.core.api_docs import (
    AUTH_ERROR_RESPONSES,
    CONFLICT_ERROR_RESPONSES,
    NOT_FOUND_ERROR_RESPONSES,
    SERVER_ERROR_RESPONSES,
    VALIDATION_ERROR_RESPONSES,
    combine_responses,
)
from app.dependencies.auth import get_current_user
from app.dependencies.pagination import PaginationDep
from app.dependencies.services import UserServiceDep
from app.schemas import Page, UpdateUserRolesRequest, UserCreate, UserPublic, UserUpdate


router = APIRouter(
    prefix='/users',
    tags=['users'],
    responses=combine_responses(
        SERVER_ERROR_RESPONSES,
        VALIDATION_ERROR_RESPONSES,
        AUTH_ERROR_RESPONSES,
    ),
)


@router.get(
    '/',
    response_model=Page[UserPublic],
    dependencies=[Security(get_current_user, scopes=['users:read'])],
)
async def list_users(service: UserServiceDep, pagination: PaginationDep):
    return await service.list(pagination)


@router.get(
    '/{user_id}',
    response_model=UserPublic,
    dependencies=[Security(get_current_user, scopes=['users:read'])],
    responses=NOT_FOUND_ERROR_RESPONSES,
)
async def get_user(user_id: int, service: UserServiceDep):
    return await service.get(user_id)


@router.post(
    '/',
    response_model=UserPublic,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Security(get_current_user, scopes=['users:write'])],
    responses=CONFLICT_ERROR_RESPONSES,
)
async def create_user(
    payload: UserCreate,
    service: UserServiceDep,
):
    return await service.create(payload)


@router.patch(
    '/{user_id}',
    response_model=UserPublic,
    dependencies=[Security(get_current_user, scopes=['users:write'])],
    responses=NOT_FOUND_ERROR_RESPONSES,
)
async def update_user(
    user_id: int,
    payload: UserUpdate,
    service: UserServiceDep,
):
    return await service.update(user_id, payload)


@router.patch(
    '/{user_id}/roles',
    response_model=UserPublic,
    dependencies=[Security(get_current_user, scopes=['users:write'])],
    responses=NOT_FOUND_ERROR_RESPONSES,
)
async def update_user_roles(
    user_id: int,
    payload: UpdateUserRolesRequest,
    service: UserServiceDep,
):
    return await service.update_roles(user_id, payload.role_names)


@router.delete(
    '/{user_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Security(get_current_user, scopes=['users:write'])],
    responses=NOT_FOUND_ERROR_RESPONSES,
)
async def delete_user(user_id: int, service: UserServiceDep):
    await service.delete(user_id)
