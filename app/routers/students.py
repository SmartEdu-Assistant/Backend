from fastapi import APIRouter, Security, status

from app.dependencies.auth import get_current_user
from app.dependencies.services import StudentServiceDep
from app.schemas import StudentCreate, StudentPublic, StudentUpdate


router = APIRouter(prefix='/students', tags=['students'])


@router.get(
    '/',
    response_model=list[StudentPublic],
    dependencies=[Security(get_current_user, scopes=['students:read'])],
)
async def list_students(service: StudentServiceDep):
    return await service.list()


@router.get(
    '/{student_id}',
    response_model=StudentPublic,
    dependencies=[Security(get_current_user, scopes=['students:read'])],
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
)
async def delete_student(student_id: int, service: StudentServiceDep):
    await service.delete(student_id)
