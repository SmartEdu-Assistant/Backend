from typing import Annotated

from fastapi import Depends

from app.models import TestCase, TestCaseCreate, TestCaseUpdate
from app.repositories import TestCaseRepository
from app.services.base import BaseService


class TestCaseService(BaseService[TestCase, TestCaseCreate, TestCaseUpdate]):
    entity_name = 'TestCase'

    def __init__(
        self,
        repository: Annotated[TestCaseRepository, Depends(TestCaseRepository)],
    ) -> None:
        super().__init__(repository)
