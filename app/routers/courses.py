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
from app.dependencies.services import CourseServiceDep
from app.schemas import CourseCreate, CoursePublic, CourseUpdate, Page


router = APIRouter(
    prefix='/courses',
    tags=['courses'],
    responses=combine_responses(
        SERVER_ERROR_RESPONSES,
        VALIDATION_ERROR_RESPONSES,
        AUTH_ERROR_RESPONSES,
    ),
)


@router.get(
    '/',
    response_model=Page[CoursePublic],
    dependencies=[Security(get_current_user, scopes=['courses:read'])],
)
async def list_courses(service: CourseServiceDep, pagination: PaginationDep):
    return await service.list(pagination)


@router.get(
    '/{course_id}',
    response_model=CoursePublic,
    dependencies=[Security(get_current_user, scopes=['courses:read'])],
    responses=NOT_FOUND_ERROR_RESPONSES,
)
async def get_course(course_id: int, service: CourseServiceDep):
    return await service.get(course_id)


@router.post(
    '/',
    response_model=CoursePublic,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Security(get_current_user, scopes=['courses:write'])],
)
async def create_course(
    payload: CourseCreate,
    service: CourseServiceDep,
):
    return await service.create(payload)


@router.patch(
    '/{course_id}',
    response_model=CoursePublic,
    dependencies=[Security(get_current_user, scopes=['courses:write'])],
    responses=NOT_FOUND_ERROR_RESPONSES,
)
async def update_course(
    course_id: int,
    payload: CourseUpdate,
    service: CourseServiceDep,
):
    return await service.update(course_id, payload)


@router.delete(
    '/{course_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Security(get_current_user, scopes=['courses:write'])],
    responses=NOT_FOUND_ERROR_RESPONSES,
)
async def delete_course(course_id: int, service: CourseServiceDep):
    await service.delete(course_id)
