from fastapi import APIRouter, status

from app.dependencies.services import GroupServiceDep
from app.schemas import GroupCreate, GroupPublic, GroupUpdate


router = APIRouter(prefix='/groups', tags=['groups'])


@router.get('/', response_model=list[GroupPublic])
async def list_groups(service: GroupServiceDep):
    return await service.list()


@router.get('/{group_id}', response_model=GroupPublic)
async def get_group(group_id: int, service: GroupServiceDep):
    return await service.get(group_id)


@router.post('/', response_model=GroupPublic, status_code=status.HTTP_201_CREATED)
async def create_group(
    payload: GroupCreate,
    service: GroupServiceDep,
):
    return await service.create(payload)


@router.patch('/{group_id}', response_model=GroupPublic)
async def update_group(
    group_id: int,
    payload: GroupUpdate,
    service: GroupServiceDep,
):
    return await service.update(group_id, payload)


@router.delete('/{group_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_group(group_id: int, service: GroupServiceDep):
    await service.delete(group_id)
