from fastapi import APIRouter, Security, status

from app.dependencies.auth import get_current_user
from app.dependencies.services import CourseServiceDep
from app.schemas import CourseCreate, CoursePublic, CourseUpdate


router = APIRouter(prefix='/courses', tags=['courses'])


@router.get(
    '/',
    response_model=list[CoursePublic],
    dependencies=[Security(get_current_user, scopes=['courses:read'])],
)
async def list_courses(service: CourseServiceDep):
    return await service.list()


@router.get(
    '/{course_id}',
    response_model=CoursePublic,
    dependencies=[Security(get_current_user, scopes=['courses:read'])],
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
)
async def delete_course(course_id: int, service: CourseServiceDep):
    await service.delete(course_id)
