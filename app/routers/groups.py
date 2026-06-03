from fastapi import APIRouter, Security, status

from app.core.api_docs import (
    AUTH_ERROR_RESPONSES,
    NOT_FOUND_ERROR_RESPONSES,
    SERVER_ERROR_RESPONSES,
    VALIDATION_ERROR_RESPONSES,
    combine_responses,
)
from app.dependencies.auth import get_current_user
from app.dependencies.pagination import PaginationDep
from app.dependencies.services import GroupServiceDep
from app.schemas import GroupCreate, GroupPublic, GroupUpdate, Page


router = APIRouter(
    prefix='/groups',
    tags=['groups'],
    responses=combine_responses(
        SERVER_ERROR_RESPONSES,
        VALIDATION_ERROR_RESPONSES,
        AUTH_ERROR_RESPONSES,
    ),
)


@router.get(
    '/',
    response_model=Page[GroupPublic],
    dependencies=[Security(get_current_user, scopes=['groups:read'])],
)
async def list_groups(service: GroupServiceDep, pagination: PaginationDep):
    return await service.list(pagination)


@router.get(
    '/{group_id}',
    response_model=GroupPublic,
    dependencies=[Security(get_current_user, scopes=['groups:read'])],
    responses=NOT_FOUND_ERROR_RESPONSES,
)
async def get_group(group_id: int, service: GroupServiceDep):
    return await service.get(group_id)


@router.post(
    '/',
    response_model=GroupPublic,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Security(get_current_user, scopes=['groups:write'])],
)
async def create_group(
    payload: GroupCreate,
    service: GroupServiceDep,
):
    return await service.create(payload)


@router.patch(
    '/{group_id}',
    response_model=GroupPublic,
    dependencies=[Security(get_current_user, scopes=['groups:write'])],
    responses=NOT_FOUND_ERROR_RESPONSES,
)
async def update_group(
    group_id: int,
    payload: GroupUpdate,
    service: GroupServiceDep,
):
    return await service.update(group_id, payload)


@router.delete(
    '/{group_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Security(get_current_user, scopes=['groups:write'])],
    responses=NOT_FOUND_ERROR_RESPONSES,
)
async def delete_group(group_id: int, service: GroupServiceDep):
    await service.delete(group_id)
