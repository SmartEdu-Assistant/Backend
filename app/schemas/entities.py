from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import ConfigDict
from sqlmodel import Field, SQLModel

from app.models import UserRole, UserStatus


class ORMBaseSchema(SQLModel):
    model_config = ConfigDict(from_attributes=True)


class UserBase(SQLModel):
    email: str = Field(max_length=255)
    first_name: str = Field(max_length=100)
    last_name: str = Field(max_length=100)
    role: UserRole = UserRole.TEACHER
    status: UserStatus = UserStatus.ACTIVE


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=255)


class UserUpdate(SQLModel):
    email: Optional[str] = Field(default=None, max_length=255)
    first_name: Optional[str] = Field(default=None, max_length=100)
    last_name: Optional[str] = Field(default=None, max_length=100)
    role: Optional[UserRole] = None
    status: Optional[UserStatus] = None
    password: Optional[str] = Field(default=None, min_length=8, max_length=255)


class UserPublic(UserBase, ORMBaseSchema):
    id: int
    created_at: datetime


class CourseBase(SQLModel):
    title: str = Field(max_length=255)
    description: Optional[str] = None
    is_active: bool = True


class CourseCreate(CourseBase):
    teacher_ids: list[int] = Field(default_factory=list)


class CourseUpdate(SQLModel):
    title: Optional[str] = Field(default=None, max_length=255)
    description: Optional[str] = None
    is_active: Optional[bool] = None
    teacher_ids: Optional[list[int]] = None


class CoursePublic(CourseBase, ORMBaseSchema):
    id: int
    created_at: datetime


class GroupBase(SQLModel):
    name: str = Field(max_length=100)
    semester: str = Field(max_length=50)
    year: int
    course_id: int


class GroupCreate(GroupBase):
    pass


class GroupUpdate(SQLModel):
    name: Optional[str] = Field(default=None, max_length=100)
    semester: Optional[str] = Field(default=None, max_length=50)
    year: Optional[int] = None
    course_id: Optional[int] = None


class GroupPublic(GroupBase, ORMBaseSchema):
    id: int
    created_at: datetime


class StudentBase(SQLModel):
    full_name: str = Field(max_length=255)
    email: Optional[str] = Field(default=None, max_length=255)
    group_id: int


class StudentCreate(StudentBase):
    pass


class StudentUpdate(SQLModel):
    full_name: Optional[str] = Field(default=None, max_length=255)
    email: Optional[str] = Field(default=None, max_length=255)
    group_id: Optional[int] = None


class StudentPublic(StudentBase, ORMBaseSchema):
    id: int
    created_at: datetime


class AssignmentBase(SQLModel):
    title: str = Field(max_length=255)
    description: str
    language: str = Field(max_length=50)
    deadline: Optional[datetime] = None
    max_score: int
    reference_solution: Optional[str] = Field(default=None, max_length=500)
    course_id: int


class AssignmentCreate(AssignmentBase):
    pass


class AssignmentUpdate(SQLModel):
    title: Optional[str] = Field(default=None, max_length=255)
    description: Optional[str] = None
    language: Optional[str] = Field(default=None, max_length=50)
    deadline: Optional[datetime] = None
    max_score: Optional[int] = None
    reference_solution: Optional[str] = Field(default=None, max_length=500)
    course_id: Optional[int] = None


class AssignmentPublic(AssignmentBase, ORMBaseSchema):
    id: int
    created_at: datetime


class TestCaseBase(SQLModel):
    assignment_id: int
    input_data: str
    expected_output: str
    weight: int


class TestCaseCreate(TestCaseBase):
    pass


class TestCaseUpdate(SQLModel):
    assignment_id: Optional[int] = None
    input_data: Optional[str] = None
    expected_output: Optional[str] = None
    weight: Optional[int] = None


class TestCasePublic(TestCaseBase, ORMBaseSchema):
    id: int
    created_at: datetime


class SubmissionBase(SQLModel):
    assignment_id: int
    student_id: int
    file_path: str = Field(max_length=500)


class SubmissionCreate(SubmissionBase):
    pass


class SubmissionUpdate(SQLModel):
    assignment_id: Optional[int] = None
    student_id: Optional[int] = None
    file_path: Optional[str] = Field(default=None, max_length=500)


class SubmissionPublic(SubmissionBase, ORMBaseSchema):
    id: int
    submitted_at: datetime


class TestResultBase(SQLModel):
    submission_id: int
    test_case_id: int
    passed: bool
    execution_time_ms: Optional[int] = None
    error_message: Optional[str] = None


class TestResultCreate(TestResultBase):
    pass


class TestResultUpdate(SQLModel):
    submission_id: Optional[int] = None
    test_case_id: Optional[int] = None
    passed: Optional[bool] = None
    execution_time_ms: Optional[int] = None
    error_message: Optional[str] = None


class TestResultPublic(TestResultBase, ORMBaseSchema):
    id: int


class PlagiarismReportBase(SQLModel):
    submission_id: int
    compared_with_id: int
    similarity_percent: float
    detected_blocks: Optional[str] = None


class PlagiarismReportCreate(PlagiarismReportBase):
    pass


class PlagiarismReportUpdate(SQLModel):
    submission_id: Optional[int] = None
    compared_with_id: Optional[int] = None
    similarity_percent: Optional[float] = None
    detected_blocks: Optional[str] = None


class PlagiarismReportPublic(PlagiarismReportBase, ORMBaseSchema):
    id: int
    created_at: datetime


class CommentBase(SQLModel):
    submission_id: int
    author_id: int
    content: str
    start_line_number: Optional[int] = None
    end_line_number: Optional[int] = None
    is_system_generated: bool = False


class CommentCreate(CommentBase):
    pass


class CommentUpdate(SQLModel):
    submission_id: Optional[int] = None
    author_id: Optional[int] = None
    content: Optional[str] = None
    start_line_number: Optional[int] = None
    end_line_number: Optional[int] = None
    is_system_generated: Optional[bool] = None


class CommentPublic(CommentBase, ORMBaseSchema):
    id: int
    created_at: datetime


class GradeBase(SQLModel):
    submission_id: int
    score: int
    max_score: int
    graded_by: int
    is_published: bool = False


class GradeCreate(GradeBase):
    pass


class GradeUpdate(SQLModel):
    submission_id: Optional[int] = None
    score: Optional[int] = None
    max_score: Optional[int] = None
    graded_by: Optional[int] = None
    is_published: Optional[bool] = None


class GradePublic(GradeBase, ORMBaseSchema):
    id: int
    graded_at: datetime
