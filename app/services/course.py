from typing import Annotated

from fastapi import Depends

from app.core.exceptions import DomainValidationError
from app.models import Course, CourseCreate, CourseUpdate, User
from app.repositories import CourseRepository, UserRepository
from app.services.base import BaseService


class CourseService(BaseService[Course, CourseCreate, CourseUpdate]):
    entity_name = 'Course'

    def __init__(
        self,
        repository: Annotated[CourseRepository, Depends(CourseRepository)],
        user_repository: Annotated[UserRepository, Depends(UserRepository)],
    ) -> None:
        super().__init__(repository)
        self.user_repository = user_repository

    async def create(self, payload: CourseCreate) -> Course:
        course = await self.repository.create(payload.model_dump(exclude={'teacher_ids'}))
        course.teachers = await self._get_teachers(payload.teacher_ids)
        return await self.repository.save(course)

    async def update(self, entity_id: int, payload: CourseUpdate) -> Course:
        course = await self.get(entity_id)
        update_data = payload.model_dump(
            exclude_unset=True,
            exclude_none=True,
            exclude={'teacher_ids'},
        )
        if update_data:
            course = await self.repository.update(course, update_data)

        if payload.teacher_ids is not None:
            course.teachers = await self._get_teachers(payload.teacher_ids)
            course = await self.repository.save(course)

        return course

    async def _get_teachers(self, teacher_ids: list[int]) -> list[User]:
        teachers = await self.user_repository.get_multi_by_ids(teacher_ids)
        if len(teachers) != len(set(teacher_ids)):
            raise DomainValidationError('One or more teachers were not found')
        return teachers
