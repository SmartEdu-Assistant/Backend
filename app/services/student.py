from typing import Annotated

from fastapi import Depends

from app.models import Student, StudentCreate, StudentUpdate
from app.repositories import StudentRepository
from app.services.base import BaseService


class StudentService(BaseService[Student, StudentCreate, StudentUpdate]):
    entity_name = 'Student'

    def __init__(
        self,
        repository: Annotated[StudentRepository, Depends(StudentRepository)],
    ) -> None:
        super().__init__(repository)
