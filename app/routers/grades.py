from fastapi import APIRouter, Depends, status

from app.dependencies.services import get_grade_service
from app.schemas import GradeCreate, GradePublic, GradeUpdate
from app.services import GradeService


router = APIRouter(prefix='/grades', tags=['grades'])


@router.get('/', response_model=list[GradePublic])
async def list_grades(service: GradeService = Depends(get_grade_service)):
    return await service.list()


@router.get('/{grade_id}', response_model=GradePublic)
async def get_grade(grade_id: int, service: GradeService = Depends(get_grade_service)):
    return await service.get(grade_id)


@router.post('/', response_model=GradePublic, status_code=status.HTTP_201_CREATED)
async def create_grade(
    payload: GradeCreate,
    service: GradeService = Depends(get_grade_service),
):
    return await service.create(payload)


@router.patch('/{grade_id}', response_model=GradePublic)
async def update_grade(
    grade_id: int,
    payload: GradeUpdate,
    service: GradeService = Depends(get_grade_service),
):
    return await service.update(grade_id, payload)


@router.delete('/{grade_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_grade(grade_id: int, service: GradeService = Depends(get_grade_service)):
    await service.delete(grade_id)
