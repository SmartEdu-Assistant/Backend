from typing import Annotated

from fastapi import Depends

from app.models import TestResult, TestResultCreate, TestResultUpdate
from app.repositories import TestResultRepository
from app.services.base import BaseService


class TestResultService(BaseService[TestResult, TestResultCreate, TestResultUpdate]):
    entity_name = 'TestResult'

    def __init__(
        self,
        repository: Annotated[TestResultRepository, Depends(TestResultRepository)],
    ) -> None:
        super().__init__(repository)
