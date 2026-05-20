from fastapi import APIRouter, status

from app.dependencies.services import UserServiceDep
from app.schemas import UserCreate, UserPublic, UserUpdate


router = APIRouter(prefix='/users', tags=['users'])


@router.get('/', response_model=list[UserPublic])
async def list_users(service: UserServiceDep):
    return await service.list()


@router.get('/{user_id}', response_model=UserPublic)
async def get_user(user_id: int, service: UserServiceDep):
    return await service.get(user_id)


@router.post('/', response_model=UserPublic, status_code=status.HTTP_201_CREATED)
async def create_user(
    payload: UserCreate,
    service: UserServiceDep,
):
    return await service.create(payload)


@router.patch('/{user_id}', response_model=UserPublic)
async def update_user(
    user_id: int,
    payload: UserUpdate,
    service: UserServiceDep,
):
    return await service.update(user_id, payload)


@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, service: UserServiceDep):
    await service.delete(user_id)
