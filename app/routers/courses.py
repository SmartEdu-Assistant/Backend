from fastapi import APIRouter, status

from app.dependencies.services import CourseServiceDep
from app.schemas import CourseCreate, CoursePublic, CourseUpdate


router = APIRouter(prefix='/courses', tags=['courses'])


@router.get('/', response_model=list[CoursePublic])
async def list_courses(service: CourseServiceDep):
    return await service.list()


@router.get('/{course_id}', response_model=CoursePublic)
async def get_course(course_id: int, service: CourseServiceDep):
    return await service.get(course_id)


@router.post('/', response_model=CoursePublic, status_code=status.HTTP_201_CREATED)
async def create_course(
    payload: CourseCreate,
    service: CourseServiceDep,
):
    return await service.create(payload)


@router.patch('/{course_id}', response_model=CoursePublic)
async def update_course(
    course_id: int,
    payload: CourseUpdate,
    service: CourseServiceDep,
):
    return await service.update(course_id, payload)


@router.delete('/{course_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(course_id: int, service: CourseServiceDep):
    await service.delete(course_id)
