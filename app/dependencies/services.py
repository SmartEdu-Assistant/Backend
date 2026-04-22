from fastapi import Depends

from app.dependencies.repositories import (
    get_assignment_repository,
    get_comment_repository,
    get_course_repository,
    get_grade_repository,
    get_group_repository,
    get_plagiarism_report_repository,
    get_student_repository,
    get_submission_repository,
    get_test_case_repository,
    get_test_result_repository,
    get_user_repository,
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
from app.services import (
    AssignmentService,
    CommentService,
    CourseService,
    GradeService,
    GroupService,
    PlagiarismReportService,
    StudentService,
    SubmissionService,
    TestCaseService,
    TestResultService,
    UserService,
)


def get_user_service(
    repository: UserRepository = Depends(get_user_repository),
) -> UserService:
    return UserService(repository)


def get_course_service(
    repository: CourseRepository = Depends(get_course_repository),
    user_repository: UserRepository = Depends(get_user_repository),
) -> CourseService:
    return CourseService(repository, user_repository)


def get_group_service(
    repository: GroupRepository = Depends(get_group_repository),
) -> GroupService:
    return GroupService(repository)


def get_student_service(
    repository: StudentRepository = Depends(get_student_repository),
) -> StudentService:
    return StudentService(repository)


def get_assignment_service(
    repository: AssignmentRepository = Depends(get_assignment_repository),
) -> AssignmentService:
    return AssignmentService(repository)


def get_test_case_service(
    repository: TestCaseRepository = Depends(get_test_case_repository),
) -> TestCaseService:
    return TestCaseService(repository)


def get_submission_service(
    repository: SubmissionRepository = Depends(get_submission_repository),
) -> SubmissionService:
    return SubmissionService(repository)


def get_test_result_service(
    repository: TestResultRepository = Depends(get_test_result_repository),
) -> TestResultService:
    return TestResultService(repository)


def get_comment_service(
    repository: CommentRepository = Depends(get_comment_repository),
) -> CommentService:
    return CommentService(repository)


def get_grade_service(
    repository: GradeRepository = Depends(get_grade_repository),
) -> GradeService:
    return GradeService(repository)


def get_plagiarism_report_service(
    repository: PlagiarismReportRepository = Depends(get_plagiarism_report_repository),
) -> PlagiarismReportService:
    return PlagiarismReportService(repository)
