from fastapi import APIRouter, Depends, status

from app.dependencies.services import get_comment_service
from app.schemas import CommentCreate, CommentPublic, CommentUpdate
from app.services import CommentService


router = APIRouter(prefix='/comments', tags=['comments'])


@router.get('/', response_model=list[CommentPublic])
async def list_comments(service: CommentService = Depends(get_comment_service)):
    return await service.list()


@router.get('/{comment_id}', response_model=CommentPublic)
async def get_comment(comment_id: int, service: CommentService = Depends(get_comment_service)):
    return await service.get(comment_id)


@router.post('/', response_model=CommentPublic, status_code=status.HTTP_201_CREATED)
async def create_comment(
    payload: CommentCreate,
    service: CommentService = Depends(get_comment_service),
):
    return await service.create(payload)


@router.patch('/{comment_id}', response_model=CommentPublic)
async def update_comment(
    comment_id: int,
    payload: CommentUpdate,
    service: CommentService = Depends(get_comment_service),
):
    return await service.update(comment_id, payload)


@router.delete('/{comment_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(comment_id: int, service: CommentService = Depends(get_comment_service)):
    await service.delete(comment_id)
