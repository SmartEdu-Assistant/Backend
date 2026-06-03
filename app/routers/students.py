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
from app.dependencies.services import StudentServiceDep
from app.schemas import Page, StudentCreate, StudentPublic, StudentUpdate


router = APIRouter(
    prefix='/students',
    tags=['students'],
    responses=combine_responses(
        SERVER_ERROR_RESPONSES,
        VALIDATION_ERROR_RESPONSES,
        AUTH_ERROR_RESPONSES,
    ),
)


@router.get(
    '/',
    response_model=Page[StudentPublic],
    dependencies=[Security(get_current_user, scopes=['students:read'])],
)
async def list_students(service: StudentServiceDep, pagination: PaginationDep):
    return await service.list(pagination)


@router.get(
    '/{student_id}',
    response_model=StudentPublic,
    dependencies=[Security(get_current_user, scopes=['students:read'])],
    responses=NOT_FOUND_ERROR_RESPONSES,
)
async def get_student(student_id: int, service: StudentServiceDep):
    return await service.get(student_id)


@router.post(
    '/',
    response_model=StudentPublic,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Security(get_current_user, scopes=['students:write'])],
)
async def create_student(
    payload: StudentCreate,
    service: StudentServiceDep,
):
    return await service.create(payload)


@router.patch(
    '/{student_id}',
    response_model=StudentPublic,
    dependencies=[Security(get_current_user, scopes=['students:write'])],
    responses=NOT_FOUND_ERROR_RESPONSES,
)
async def update_student(
    student_id: int,
    payload: StudentUpdate,
    service: StudentServiceDep,
):
    return await service.update(student_id, payload)


@router.delete(
    '/{student_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Security(get_current_user, scopes=['students:write'])],
    responses=NOT_FOUND_ERROR_RESPONSES,
)
async def delete_student(student_id: int, service: StudentServiceDep):
    await service.delete(student_id)
