from fastapi import APIRouter, Depends, status

from app.dependencies.services import get_assignment_service
from app.schemas import AssignmentCreate, AssignmentPublic, AssignmentUpdate
from app.services import AssignmentService


router = APIRouter(prefix='/assignments', tags=['assignments'])


@router.get('/', response_model=list[AssignmentPublic])
async def list_assignments(service: AssignmentService = Depends(get_assignment_service)):
    return await service.list()


@router.get('/{assignment_id}', response_model=AssignmentPublic)
async def get_assignment(
    assignment_id: int,
    service: AssignmentService = Depends(get_assignment_service),
):
    return await service.get(assignment_id)


@router.post('/', response_model=AssignmentPublic, status_code=status.HTTP_201_CREATED)
async def create_assignment(
    payload: AssignmentCreate,
    service: AssignmentService = Depends(get_assignment_service),
):
    return await service.create(payload)


@router.patch('/{assignment_id}', response_model=AssignmentPublic)
async def update_assignment(
    assignment_id: int,
    payload: AssignmentUpdate,
    service: AssignmentService = Depends(get_assignment_service),
):
    return await service.update(assignment_id, payload)


@router.delete('/{assignment_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_assignment(
    assignment_id: int,
    service: AssignmentService = Depends(get_assignment_service),
):
    await service.delete(assignment_id)
