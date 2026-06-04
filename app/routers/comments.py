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
from app.dependencies.services import CommentServiceDep
from app.schemas import CommentCreate, CommentPublic, CommentUpdate, Page


router = APIRouter(
    prefix='/comments',
    tags=['comments'],
    responses=combine_responses(
        SERVER_ERROR_RESPONSES,
        VALIDATION_ERROR_RESPONSES,
        AUTH_ERROR_RESPONSES,
    ),
)


@router.get(
    '/',
    response_model=Page[CommentPublic],
    dependencies=[Security(get_current_user, scopes=['comments:read'])],
)
async def list_comments(service: CommentServiceDep, pagination: PaginationDep):
    return await service.list(pagination)


@router.get(
    '/{comment_id}',
    response_model=CommentPublic,
    dependencies=[Security(get_current_user, scopes=['comments:read'])],
    responses=NOT_FOUND_ERROR_RESPONSES,
)
async def get_comment(comment_id: int, service: CommentServiceDep):
    return await service.get(comment_id)


@router.post(
    '/',
    response_model=CommentPublic,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Security(get_current_user, scopes=['comments:write'])],
)
async def create_comment(
    payload: CommentCreate,
    service: CommentServiceDep,
):
    return await service.create(payload)


@router.patch(
    '/{comment_id}',
    response_model=CommentPublic,
    dependencies=[Security(get_current_user, scopes=['comments:write'])],
    responses=NOT_FOUND_ERROR_RESPONSES,
)
async def update_comment(
    comment_id: int,
    payload: CommentUpdate,
    service: CommentServiceDep,
):
    return await service.update(comment_id, payload)


@router.delete(
    '/{comment_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Security(get_current_user, scopes=['comments:write'])],
    responses=NOT_FOUND_ERROR_RESPONSES,
)
async def delete_comment(comment_id: int, service: CommentServiceDep):
    await service.delete(comment_id)
