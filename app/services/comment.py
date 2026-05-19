from typing import Annotated

from fastapi import Depends

from app.models import Comment, CommentCreate, CommentUpdate
from app.repositories import CommentRepository
from app.services.base import BaseService


class CommentService(BaseService[Comment, CommentCreate, CommentUpdate]):
    entity_name = 'Comment'

    def __init__(
        self,
        repository: Annotated[CommentRepository, Depends(CommentRepository)],
    ) -> None:
        super().__init__(repository)
