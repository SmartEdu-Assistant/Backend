from fastapi import APIRouter, status

from app.dependencies.services import CommentServiceDep
from app.schemas import CommentCreate, CommentPublic, CommentUpdate


router = APIRouter(prefix='/comments', tags=['comments'])


@router.get('/', response_model=list[CommentPublic])
async def list_comments(service: CommentServiceDep):
    return await service.list()


@router.get('/{comment_id}', response_model=CommentPublic)
async def get_comment(comment_id: int, service: CommentServiceDep):
    return await service.get(comment_id)


@router.post('/', response_model=CommentPublic, status_code=status.HTTP_201_CREATED)
async def create_comment(
    payload: CommentCreate,
    service: CommentServiceDep,
):
    return await service.create(payload)


@router.patch('/{comment_id}', response_model=CommentPublic)
async def update_comment(
    comment_id: int,
    payload: CommentUpdate,
    service: CommentServiceDep,
):
    return await service.update(comment_id, payload)


@router.delete('/{comment_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(comment_id: int, service: CommentServiceDep):
    await service.delete(comment_id)
