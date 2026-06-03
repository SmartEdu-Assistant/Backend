from fastapi import APIRouter, Security, status

from app.dependencies.auth import get_current_user
from app.dependencies.services import GradeServiceDep
from app.schemas import GradeCreate, GradePublic, GradeUpdate


router = APIRouter(prefix='/grades', tags=['grades'])


@router.get(
    '/',
    response_model=list[GradePublic],
    dependencies=[Security(get_current_user, scopes=['grades:read'])],
)
async def list_grades(service: GradeServiceDep):
    return await service.list()


@router.get(
    '/{grade_id}',
    response_model=GradePublic,
    dependencies=[Security(get_current_user, scopes=['grades:read'])],
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
)
async def delete_grade(grade_id: int, service: GradeServiceDep):
    await service.delete(grade_id)
