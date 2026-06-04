from typing import Annotated

from fastapi import Depends

from app.services import (
    AuthService,
    AssignmentService,
    CommentService,
    CourseService,
    EmailNotificationService,
    GradeService,
    GroupService,
    PlagiarismReportService,
    StudentService,
    SubmissionService,
    TestCaseService,
    TestResultService,
    UserService,
)

AuthServiceDep = Annotated[AuthService, Depends(AuthService)]
AssignmentServiceDep = Annotated[AssignmentService, Depends(AssignmentService)]
CommentServiceDep = Annotated[CommentService, Depends(CommentService)]
CourseServiceDep = Annotated[CourseService, Depends(CourseService)]
EmailNotificationServiceDep = Annotated[
    EmailNotificationService,
    Depends(EmailNotificationService),
]
GradeServiceDep = Annotated[GradeService, Depends(GradeService)]
GroupServiceDep = Annotated[GroupService, Depends(GroupService)]
PlagiarismReportServiceDep = Annotated[
    PlagiarismReportService,
    Depends(PlagiarismReportService),
]
StudentServiceDep = Annotated[StudentService, Depends(StudentService)]
SubmissionServiceDep = Annotated[SubmissionService, Depends(SubmissionService)]
TestCaseServiceDep = Annotated[TestCaseService, Depends(TestCaseService)]
TestResultServiceDep = Annotated[TestResultService, Depends(TestResultService)]
UserServiceDep = Annotated[UserService, Depends(UserService)]

__all__ = [
    'AuthServiceDep',
    'AssignmentServiceDep',
    'CommentServiceDep',
    'CourseServiceDep',
    'EmailNotificationServiceDep',
    'GradeServiceDep',
    'GroupServiceDep',
    'PlagiarismReportServiceDep',
    'StudentServiceDep',
    'SubmissionServiceDep',
    'TestCaseServiceDep',
    'TestResultServiceDep',
    'UserServiceDep',
]
