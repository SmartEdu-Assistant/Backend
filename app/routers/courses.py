from fastapi import APIRouter, Depends, status

from app.dependencies.services import get_course_service
from app.schemas import CourseCreate, CoursePublic, CourseUpdate
from app.services import CourseService


router = APIRouter(prefix='/courses', tags=['courses'])


@router.get('/', response_model=list[CoursePublic])
async def list_courses(service: CourseService = Depends(get_course_service)):
    return await service.list()


@router.get('/{course_id}', response_model=CoursePublic)
async def get_course(course_id: int, service: CourseService = Depends(get_course_service)):
    return await service.get(course_id)


@router.post('/', response_model=CoursePublic, status_code=status.HTTP_201_CREATED)
async def create_course(
    payload: CourseCreate,
    service: CourseService = Depends(get_course_service),
):
    return await service.create(payload)


@router.patch('/{course_id}', response_model=CoursePublic)
async def update_course(
    course_id: int,
    payload: CourseUpdate,
    service: CourseService = Depends(get_course_service),
):
    return await service.update(course_id, payload)


@router.delete('/{course_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(course_id: int, service: CourseService = Depends(get_course_service)):
    await service.delete(course_id)
