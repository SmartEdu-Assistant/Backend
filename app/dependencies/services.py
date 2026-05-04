from typing import Annotated

from fastapi import Depends

from app.dependencies.repositories import (
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

UserRepositoryDep = Annotated[UserRepository, Depends(UserRepository)]
CourseRepositoryDep = Annotated[CourseRepository, Depends(CourseRepository)]
GroupRepositoryDep = Annotated[GroupRepository, Depends(GroupRepository)]
StudentRepositoryDep = Annotated[StudentRepository, Depends(StudentRepository)]
AssignmentRepositoryDep = Annotated[AssignmentRepository, Depends(AssignmentRepository)]
TestCaseRepositoryDep = Annotated[TestCaseRepository, Depends(TestCaseRepository)]
SubmissionRepositoryDep = Annotated[SubmissionRepository, Depends(SubmissionRepository)]
TestResultRepositoryDep = Annotated[TestResultRepository, Depends(TestResultRepository)]
CommentRepositoryDep = Annotated[CommentRepository, Depends(CommentRepository)]
GradeRepositoryDep = Annotated[GradeRepository, Depends(GradeRepository)]
PlagiarismReportRepositoryDep = Annotated[
    PlagiarismReportRepository,
    Depends(PlagiarismReportRepository),
]


def get_user_service(
    repository: UserRepositoryDep,
) -> UserService:
    return UserService(repository)


def get_course_service(
    repository: CourseRepositoryDep,
    user_repository: UserRepositoryDep,
) -> CourseService:
    return CourseService(repository, user_repository)


def get_group_service(
    repository: GroupRepositoryDep,
) -> GroupService:
    return GroupService(repository)


def get_student_service(
    repository: StudentRepositoryDep,
) -> StudentService:
    return StudentService(repository)


def get_assignment_service(
    repository: AssignmentRepositoryDep,
) -> AssignmentService:
    return AssignmentService(repository)


def get_test_case_service(
    repository: TestCaseRepositoryDep,
) -> TestCaseService:
    return TestCaseService(repository)


def get_submission_service(
    repository: SubmissionRepositoryDep,
) -> SubmissionService:
    return SubmissionService(repository)


def get_test_result_service(
    repository: TestResultRepositoryDep,
) -> TestResultService:
    return TestResultService(repository)


def get_comment_service(
    repository: CommentRepositoryDep,
) -> CommentService:
    return CommentService(repository)


def get_grade_service(
    repository: GradeRepositoryDep,
) -> GradeService:
    return GradeService(repository)


def get_plagiarism_report_service(
    repository: PlagiarismReportRepositoryDep,
) -> PlagiarismReportService:
    return PlagiarismReportService(repository)
