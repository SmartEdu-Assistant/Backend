from typing import Annotated

from fastapi import Depends

from app.models import Submission, SubmissionCreate, SubmissionUpdate
from app.repositories import SubmissionRepository
from app.services.base import BaseService


class SubmissionService(BaseService[Submission, SubmissionCreate, SubmissionUpdate]):
    entity_name = 'Submission'

    def __init__(
        self,
        repository: Annotated[SubmissionRepository, Depends(SubmissionRepository)],
    ) -> None:
        super().__init__(repository)
