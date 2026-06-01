from fastapi import APIRouter, Security, status

from app.dependencies.auth import get_current_user
from app.dependencies.services import AssignmentServiceDep
from app.schemas import AssignmentCreate, AssignmentPublic, AssignmentUpdate


router = APIRouter(prefix='/assignments', tags=['assignments'])


@router.get(
    '/',
    response_model=list[AssignmentPublic],
    dependencies=[Security(get_current_user, scopes=['assignments:read'])],
)
async def list_assignments(service: AssignmentServiceDep):
    return await service.list()


@router.get(
    '/{assignment_id}',
    response_model=AssignmentPublic,
    dependencies=[Security(get_current_user, scopes=['assignments:read'])],
)
async def get_assignment(assignment_id: int, service: AssignmentServiceDep):
    return await service.get(assignment_id)


@router.post(
    '/',
    response_model=AssignmentPublic,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Security(get_current_user, scopes=['assignments:write'])],
)
async def create_assignment(
    payload: AssignmentCreate,
    service: AssignmentServiceDep,
):
    return await service.create(payload)


@router.patch(
    '/{assignment_id}',
    response_model=AssignmentPublic,
    dependencies=[Security(get_current_user, scopes=['assignments:write'])],
)
async def update_assignment(
    assignment_id: int,
    payload: AssignmentUpdate,
    service: AssignmentServiceDep,
):
    return await service.update(assignment_id, payload)


@router.delete(
    '/{assignment_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Security(get_current_user, scopes=['assignments:write'])],
)
async def delete_assignment(assignment_id: int, service: AssignmentServiceDep):
    await service.delete(assignment_id)
