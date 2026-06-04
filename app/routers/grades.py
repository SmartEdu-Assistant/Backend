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
from app.dependencies.services import GradeServiceDep
from app.schemas import GradeCreate, GradePublic, GradeUpdate, Page


router = APIRouter(
    prefix='/grades',
    tags=['grades'],
    responses=combine_responses(
        SERVER_ERROR_RESPONSES,
        VALIDATION_ERROR_RESPONSES,
        AUTH_ERROR_RESPONSES,
    ),
)


@router.get(
    '/',
    response_model=Page[GradePublic],
    dependencies=[Security(get_current_user, scopes=['grades:read'])],
)
async def list_grades(service: GradeServiceDep, pagination: PaginationDep):
    return await service.list(pagination)


@router.get(
    '/{grade_id}',
    response_model=GradePublic,
    dependencies=[Security(get_current_user, scopes=['grades:read'])],
    responses=NOT_FOUND_ERROR_RESPONSES,
)
async def get_grade(grade_id: int, service: GradeServiceDep):
    return await service.get(grade_id)


@router.post(
    '/',
    response_model=GradePublic,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Security(get_current_user, scopes=['grades:write'])],
)
async def create_grade(
    payload: GradeCreate,
    service: GradeServiceDep,
):
    return await service.create(payload)


@router.patch(
    '/{grade_id}',
    response_model=GradePublic,
    dependencies=[Security(get_current_user, scopes=['grades:write'])],
    responses=NOT_FOUND_ERROR_RESPONSES,
)
async def update_grade(
    grade_id: int,
    payload: GradeUpdate,
    service: GradeServiceDep,
):
    return await service.update(grade_id, payload)


@router.delete(
    '/{grade_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Security(get_current_user, scopes=['grades:write'])],
    responses=NOT_FOUND_ERROR_RESPONSES,
)
async def delete_grade(grade_id: int, service: GradeServiceDep):
    await service.delete(grade_id)
