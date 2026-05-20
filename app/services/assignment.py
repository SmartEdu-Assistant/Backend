from typing import Annotated

from fastapi import Depends

from app.models import Assignment, AssignmentCreate, AssignmentUpdate
from app.repositories import AssignmentRepository
from app.services.base import BaseService


class AssignmentService(BaseService[Assignment, AssignmentCreate, AssignmentUpdate]):
    entity_name = 'Assignment'

    def __init__(
        self,
        repository: Annotated[AssignmentRepository, Depends(AssignmentRepository)],
    ) -> None:
        super().__init__(repository)
