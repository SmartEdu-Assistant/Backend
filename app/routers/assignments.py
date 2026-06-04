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
from app.dependencies.services import AssignmentServiceDep
from app.schemas import AssignmentCreate, AssignmentPublic, AssignmentUpdate, Page


router = APIRouter(
    prefix='/assignments',
    tags=['assignments'],
    responses=combine_responses(
        SERVER_ERROR_RESPONSES,
        VALIDATION_ERROR_RESPONSES,
        AUTH_ERROR_RESPONSES,
    ),
)


@router.get(
    '/',
    response_model=Page[AssignmentPublic],
    dependencies=[Security(get_current_user, scopes=['assignments:read'])],
)
async def list_assignments(service: AssignmentServiceDep, pagination: PaginationDep):
    return await service.list(pagination)


@router.get(
    '/{assignment_id}',
    response_model=AssignmentPublic,
    dependencies=[Security(get_current_user, scopes=['assignments:read'])],
    responses=NOT_FOUND_ERROR_RESPONSES,
)
async def get_assignment(assignment_id: int, service: AssignmentServiceDep):
    return await service.get(assignment_id)


@router.post(
    '/',
    response_model=AssignmentPublic,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Security(get_current_user, scopes=['assignments:write'])],
)
async def create_assignment(
    payload: AssignmentCreate,
    service: AssignmentServiceDep,
):
    return await service.create(payload)


@router.patch(
    '/{assignment_id}',
    response_model=AssignmentPublic,
    dependencies=[Security(get_current_user, scopes=['assignments:write'])],
    responses=NOT_FOUND_ERROR_RESPONSES,
)
async def update_assignment(
    assignment_id: int,
    payload: AssignmentUpdate,
    service: AssignmentServiceDep,
):
    return await service.update(assignment_id, payload)


@router.delete(
    '/{assignment_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Security(get_current_user, scopes=['assignments:write'])],
    responses=NOT_FOUND_ERROR_RESPONSES,
)
async def delete_assignment(assignment_id: int, service: AssignmentServiceDep):
    await service.delete(assignment_id)
