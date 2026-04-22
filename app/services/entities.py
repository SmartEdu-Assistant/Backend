from app.core.exceptions import DomainValidationError
from app.core.security import get_password_hash
from app.models import (
    Assignment,
    Comment,
    Course,
    Grade,
    Group,
    PlagiarismReport,
    Student,
    Submission,
    TestCase,
    TestResult,
    User,
)
from app.repositories import (
    AssignmentRepository,
    CommentRepository,
    CourseRepository,
    GradeRepository,
    GroupRepository,
    PlagiarismReportRepository,
    StudentRepository,
    SubmissionRepository,
    TestCaseRepository,
    TestResultRepository,
    UserRepository,
)
from app.schemas import (
    AssignmentCreate,
    AssignmentUpdate,
    CommentCreate,
    CommentUpdate,
    CourseCreate,
    CourseUpdate,
    GradeCreate,
    GradeUpdate,
    GroupCreate,
    GroupUpdate,
    PlagiarismReportCreate,
    PlagiarismReportUpdate,
    StudentCreate,
    StudentUpdate,
    SubmissionCreate,
    SubmissionUpdate,
    TestCaseCreate,
    TestCaseUpdate,
    TestResultCreate,
    TestResultUpdate,
    UserCreate,
    UserUpdate,
)
from app.services.base import BaseService


class UserService(BaseService[User, UserCreate, UserUpdate]):
    entity_name = 'User'

    def __init__(self, repository: UserRepository) -> None:
        super().__init__(repository)

    async def create(self, payload: UserCreate) -> User:
        user_data = payload.model_dump(exclude={'password'})
        user_data['password_hash'] = get_password_hash(payload.password)
        return await self.repository.create(user_data)

    async def update(self, entity_id: int, payload: UserUpdate) -> User:
        update_data = payload.model_dump(exclude_unset=True, exclude_none=True, exclude={'password'})
        if payload.password is not None:
            update_data['password_hash'] = get_password_hash(payload.password)
        entity = await self.get(entity_id)
        return await self.repository.update(entity, update_data)


class CourseService(BaseService[Course, CourseCreate, CourseUpdate]):
    entity_name = 'Course'

    def __init__(
        self,
        repository: CourseRepository,
        user_repository: UserRepository,
    ) -> None:
        super().__init__(repository)
        self.user_repository = user_repository

    async def create(self, payload: CourseCreate) -> Course:
        course = await self.repository.create(payload.model_dump(exclude={'teacher_ids'}))
        course.teachers = await self._get_teachers(payload.teacher_ids)
        return await self.repository.save(course)

    async def update(self, entity_id: int, payload: CourseUpdate) -> Course:
        course = await self.get(entity_id)
        update_data = payload.model_dump(exclude_unset=True, exclude_none=True, exclude={'teacher_ids'})
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


class GroupService(BaseService[Group, GroupCreate, GroupUpdate]):
    entity_name = 'Group'

    def __init__(self, repository: GroupRepository) -> None:
        super().__init__(repository)


class StudentService(BaseService[Student, StudentCreate, StudentUpdate]):
    entity_name = 'Student'

    def __init__(self, repository: StudentRepository) -> None:
        super().__init__(repository)


class AssignmentService(BaseService[Assignment, AssignmentCreate, AssignmentUpdate]):
    entity_name = 'Assignment'

    def __init__(self, repository: AssignmentRepository) -> None:
        super().__init__(repository)


class TestCaseService(BaseService[TestCase, TestCaseCreate, TestCaseUpdate]):
    entity_name = 'TestCase'

    def __init__(self, repository: TestCaseRepository) -> None:
        super().__init__(repository)


class SubmissionService(BaseService[Submission, SubmissionCreate, SubmissionUpdate]):
    entity_name = 'Submission'

    def __init__(self, repository: SubmissionRepository) -> None:
        super().__init__(repository)


class TestResultService(BaseService[TestResult, TestResultCreate, TestResultUpdate]):
    entity_name = 'TestResult'

    def __init__(self, repository: TestResultRepository) -> None:
        super().__init__(repository)


class CommentService(BaseService[Comment, CommentCreate, CommentUpdate]):
    entity_name = 'Comment'

    def __init__(self, repository: CommentRepository) -> None:
        super().__init__(repository)


class GradeService(BaseService[Grade, GradeCreate, GradeUpdate]):
    entity_name = 'Grade'

    def __init__(self, repository: GradeRepository) -> None:
        super().__init__(repository)


class PlagiarismReportService(
    BaseService[PlagiarismReport, PlagiarismReportCreate, PlagiarismReportUpdate]
):
    entity_name = 'PlagiarismReport'

    def __init__(self, repository: PlagiarismReportRepository) -> None:
        super().__init__(repository)
