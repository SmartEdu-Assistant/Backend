from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.dependencies.db import get_session
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


def get_user_repository(session: AsyncSession = Depends(get_session)) -> UserRepository:
    return UserRepository(session)


def get_course_repository(session: AsyncSession = Depends(get_session)) -> CourseRepository:
    return CourseRepository(session)


def get_group_repository(session: AsyncSession = Depends(get_session)) -> GroupRepository:
    return GroupRepository(session)


def get_student_repository(session: AsyncSession = Depends(get_session)) -> StudentRepository:
    return StudentRepository(session)


def get_assignment_repository(
    session: AsyncSession = Depends(get_session),
) -> AssignmentRepository:
    return AssignmentRepository(session)


def get_test_case_repository(session: AsyncSession = Depends(get_session)) -> TestCaseRepository:
    return TestCaseRepository(session)


def get_submission_repository(
    session: AsyncSession = Depends(get_session),
) -> SubmissionRepository:
    return SubmissionRepository(session)


def get_test_result_repository(
    session: AsyncSession = Depends(get_session),
) -> TestResultRepository:
    return TestResultRepository(session)


def get_comment_repository(session: AsyncSession = Depends(get_session)) -> CommentRepository:
    return CommentRepository(session)


def get_grade_repository(session: AsyncSession = Depends(get_session)) -> GradeRepository:
    return GradeRepository(session)


def get_plagiarism_report_repository(
    session: AsyncSession = Depends(get_session),
) -> PlagiarismReportRepository:
    return PlagiarismReportRepository(session)
