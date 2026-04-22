from fastapi import APIRouter, Depends, status

from app.dependencies.services import get_user_service
from app.schemas import UserCreate, UserPublic, UserUpdate
from app.services import UserService


router = APIRouter(prefix='/users', tags=['users'])


@router.get('/', response_model=list[UserPublic])
async def list_users(service: UserService = Depends(get_user_service)):
    return await service.list()


@router.get('/{user_id}', response_model=UserPublic)
async def get_user(user_id: int, service: UserService = Depends(get_user_service)):
    return await service.get(user_id)


@router.post('/', response_model=UserPublic, status_code=status.HTTP_201_CREATED)
async def create_user(
    payload: UserCreate,
    service: UserService = Depends(get_user_service),
):
    return await service.create(payload)


@router.patch('/{user_id}', response_model=UserPublic)
async def update_user(
    user_id: int,
    payload: UserUpdate,
    service: UserService = Depends(get_user_service),
):
    return await service.update(user_id, payload)


@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, service: UserService = Depends(get_user_service)):
    await service.delete(user_id)
