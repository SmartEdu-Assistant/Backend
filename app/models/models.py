from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel


class UserRole(str, Enum):
    ADMIN = "ADMIN"
    TEACHER = "TEACHER"


class UserStatus(str, Enum):
    ACTIVE = "ACTIVE"
    BLOCKED = "BLOCKED"


class CourseTeacherLink(SQLModel, table=True):
    __tablename__ = "course_teacher_link"

    course_id: Optional[int] = Field(
        default=None,
        foreign_key="courses.id",
        primary_key=True,
    )
    user_id: Optional[int] = Field(
        default=None,
        foreign_key="users.id",
        primary_key=True,
    )


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True, max_length=255)
    password_hash: str = Field(max_length=255)
    first_name: str = Field(max_length=100)
    last_name: str = Field(max_length=100)
    role: UserRole = Field(max_length=30)
    status: UserStatus = Field(max_length=30)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    courses: list["Course"] = Relationship(
        back_populates="teachers",
        link_model=CourseTeacherLink,
    )


class Course(SQLModel, table=True):
    __tablename__ = "courses"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=255)
    description: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)

    teachers: list[User] = Relationship(
        back_populates="courses",
        link_model=CourseTeacherLink,
    )
    groups: list["Group"] = Relationship(back_populates="course")
    assignments: list["Assignment"] = Relationship(back_populates="course")


class Group(SQLModel, table=True):
    __tablename__ = "groups"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)
    semester: str = Field(max_length=50)
    year: int
    course_id: int = Field(foreign_key="courses.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    course: Optional[Course] = Relationship(back_populates="groups")
    students: list["Student"] = Relationship(back_populates="group")


class Student(SQLModel, table=True):
    __tablename__ = "students"

    id: Optional[int] = Field(default=None, primary_key=True)
    full_name: str = Field(max_length=255)
    email: Optional[str] = Field(default=None, max_length=255)
    group_id: int = Field(foreign_key="groups.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    group: Optional[Group] = Relationship(back_populates="students")
    submissions: list["Submission"] = Relationship(back_populates="student")


class Assignment(SQLModel, table=True):
    __tablename__ = "assignments"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=255)
    description: str
    language: str = Field(max_length=50)
    deadline: Optional[datetime] = Field(default=None)
    max_score: int
    reference_solution: Optional[str] = Field(default=None, max_length=500)
    course_id: int = Field(foreign_key="courses.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    course: Optional[Course] = Relationship(back_populates="assignments")
    test_cases: list["TestCase"] = Relationship(back_populates="assignment")
    submissions: list["Submission"] = Relationship(back_populates="assignment")


class TestCase(SQLModel, table=True):
    __tablename__ = "test_cases"

    id: Optional[int] = Field(default=None, primary_key=True)
    assignment_id: int = Field(foreign_key="assignments.id")
    input_data: str
    expected_output: str
    weight: int
    created_at: datetime = Field(default_factory=datetime.utcnow)

    assignment: Optional[Assignment] = Relationship(back_populates="test_cases")
    test_results: list["TestResult"] = Relationship(back_populates="test_case")


class Submission(SQLModel, table=True):
    __tablename__ = "submissions"

    id: Optional[int] = Field(default=None, primary_key=True)
    assignment_id: int = Field(foreign_key="assignments.id")
    student_id: int = Field(foreign_key="students.id")
    file_path: str = Field(max_length=500)
    submitted_at: datetime = Field(default_factory=datetime.utcnow)

    assignment: Optional[Assignment] = Relationship(back_populates="submissions")
    student: Optional[Student] = Relationship(back_populates="submissions")
    test_results: list["TestResult"] = Relationship(back_populates="submission")
    comments: list["Comment"] = Relationship(back_populates="submission")
    grades: list["Grade"] = Relationship(back_populates="submission")


class TestResult(SQLModel, table=True):
    __tablename__ = "test_results"

    id: Optional[int] = Field(default=None, primary_key=True)
    submission_id: int = Field(foreign_key="submissions.id")
    test_case_id: int = Field(foreign_key="test_cases.id")
    passed: bool
    execution_time_ms: Optional[int] = Field(default=None)
    error_message: Optional[str] = Field(default=None)

    submission: Optional[Submission] = Relationship(back_populates="test_results")
    test_case: Optional[TestCase] = Relationship(back_populates="test_results")


class PlagiarismReport(SQLModel, table=True):
    __tablename__ = "plagiarism_reports"

    id: Optional[int] = Field(default=None, primary_key=True)
    submission_id: int = Field(foreign_key="submissions.id")
    compared_with_id: int = Field(foreign_key="submissions.id")
    similarity_percent: float
    detected_blocks: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Comment(SQLModel, table=True):
    __tablename__ = "comments"

    id: Optional[int] = Field(default=None, primary_key=True)
    submission_id: int = Field(foreign_key="submissions.id")
    author_id: int = Field(foreign_key="users.id")
    content: str
    start_line_number: Optional[int] = Field(default=None)
    end_line_number: Optional[int] = Field(default=None)
    is_system_generated: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    submission: Optional[Submission] = Relationship(back_populates="comments")


class Grade(SQLModel, table=True):
    __tablename__ = "grades"

    id: Optional[int] = Field(default=None, primary_key=True)
    submission_id: int = Field(foreign_key="submissions.id", unique=True)
    score: int
    max_score: int
    graded_by: int = Field(foreign_key="users.id")
    graded_at: datetime = Field(default_factory=datetime.utcnow)
    is_published: bool = Field(default=False)

    submission: Optional[Submission] = Relationship(back_populates="grades")
