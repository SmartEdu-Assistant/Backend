from app.dependencies.db import get_session
from app.dependencies.services import (
    get_assignment_service,
    get_comment_service,
    get_course_service,
    get_grade_service,
    get_group_service,
    get_plagiarism_report_service,
    get_student_service,
    get_submission_service,
    get_test_case_service,
    get_test_result_service,
    get_user_service,
)

__all__ = [
    'get_assignment_service',
    'get_comment_service',
    'get_course_service',
    'get_grade_service',
    'get_group_service',
    'get_plagiarism_report_service',
    'get_session',
    'get_student_service',
    'get_submission_service',
    'get_test_case_service',
    'get_test_result_service',
    'get_user_service',
]
