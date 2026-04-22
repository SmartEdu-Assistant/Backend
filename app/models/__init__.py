from app.models.assignment import Assignment, TestCase
from app.models.base import BaseTableModel, TimestampedModel, UserRole, UserStatus
from app.models.course import Course
from app.models.student import Group, Student
from app.models.submission import (
    Comment,
    Grade,
    PlagiarismReport,
    Submission,
    TestResult,
)
from app.models.user import (
    CourseTeacherLink,
    User,
)

__all__ = [
    'BaseTableModel',
    'Assignment',
    'Comment',
    'Course',
    'CourseTeacherLink',
    'Grade',
    'Group',
    'PlagiarismReport',
    'Student',
    'Submission',
    'TestCase',
    'TestResult',
    'TimestampedModel',
    'User',
    'UserRole',
    'UserStatus',
]
