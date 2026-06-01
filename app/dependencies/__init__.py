from app.dependencies.db import get_session
from app.dependencies.services import (
    AuthServiceDep,
    AssignmentServiceDep,
    CommentServiceDep,
    CourseServiceDep,
    GradeServiceDep,
    GroupServiceDep,
    PlagiarismReportServiceDep,
    StudentServiceDep,
    SubmissionServiceDep,
    TestCaseServiceDep,
    TestResultServiceDep,
    UserServiceDep,
)

__all__ = [
    'AuthServiceDep',
    'AssignmentServiceDep',
    'CommentServiceDep',
    'CourseServiceDep',
    'GradeServiceDep',
    'GroupServiceDep',
    'PlagiarismReportServiceDep',
    'get_session',
    'StudentServiceDep',
    'SubmissionServiceDep',
    'TestCaseServiceDep',
    'TestResultServiceDep',
    'UserServiceDep',
]
