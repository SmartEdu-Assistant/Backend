from fastapi import APIRouter, Security, status

from app.dependencies.auth import get_current_user
from app.dependencies.services import UserServiceDep
from app.schemas import UpdateUserRolesRequest, UserCreate, UserPublic, UserUpdate


router = APIRouter(prefix='/users', tags=['users'])


@router.get(
    '/',
    response_model=list[UserPublic],
    dependencies=[Security(get_current_user, scopes=['users:read'])],
)
async def list_users(service: UserServiceDep):
    return await service.list()


@router.get(
    '/{user_id}',
    response_model=UserPublic,
    dependencies=[Security(get_current_user, scopes=['users:read'])],
)
async def get_user(user_id: int, service: UserServiceDep):
    return await service.get(user_id)


@router.post(
    '/',
    response_model=UserPublic,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Security(get_current_user, scopes=['users:write'])],
)
async def create_user(
    payload: UserCreate,
    service: UserServiceDep,
):
    return await service.create(payload)


@router.patch(
    '/{user_id}',
    response_model=UserPublic,
    dependencies=[Security(get_current_user, scopes=['users:write'])],
)
async def update_user(
    user_id: int,
    payload: UserUpdate,
    service: UserServiceDep,
):
    return await service.update(user_id, payload)


@router.patch(
    '/{user_id}/roles',
    response_model=UserPublic,
    dependencies=[Security(get_current_user, scopes=['users:write'])],
)
async def update_user_roles(
    user_id: int,
    payload: UpdateUserRolesRequest,
    service: UserServiceDep,
):
    return await service.update_roles(user_id, payload.role_names)


@router.delete(
    '/{user_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Security(get_current_user, scopes=['users:write'])],
)
async def delete_user(user_id: int, service: UserServiceDep):
    await service.delete(user_id)
