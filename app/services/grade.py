from typing import Annotated

from fastapi import Depends

from app.models import Grade, GradeCreate, GradeUpdate
from app.repositories import GradeRepository
from app.services.base import BaseService


class GradeService(BaseService[Grade, GradeCreate, GradeUpdate]):
    entity_name = 'Grade'

    def __init__(
        self,
        repository: Annotated[GradeRepository, Depends(GradeRepository)],
    ) -> None:
        super().__init__(repository)
