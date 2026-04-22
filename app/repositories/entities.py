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
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    model = User


class CourseRepository(BaseRepository[Course]):
    model = Course


class GroupRepository(BaseRepository[Group]):
    model = Group


class StudentRepository(BaseRepository[Student]):
    model = Student


class AssignmentRepository(BaseRepository[Assignment]):
    model = Assignment


class TestCaseRepository(BaseRepository[TestCase]):
    model = TestCase


class SubmissionRepository(BaseRepository[Submission]):
    model = Submission


class TestResultRepository(BaseRepository[TestResult]):
    model = TestResult


class CommentRepository(BaseRepository[Comment]):
    model = Comment


class GradeRepository(BaseRepository[Grade]):
    model = Grade


class PlagiarismReportRepository(BaseRepository[PlagiarismReport]):
    model = PlagiarismReport
