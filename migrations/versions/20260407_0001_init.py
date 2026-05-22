"""initial schema

Revision ID: 20260407_0001
Revises:
Create Date: 2026-04-07 00:00:00
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = '20260407_0001'
down_revision = None
branch_labels = None
depends_on = None


user_role_enum = postgresql.ENUM('ADMIN', 'TEACHER', name='userrole', create_type=False)
user_status_enum = postgresql.ENUM('ACTIVE', 'BLOCKED', name='userstatus', create_type=False)


def upgrade() -> None:
    bind = op.get_bind()
    user_role_enum.create(bind, checkfirst=True)
    user_status_enum.create(bind, checkfirst=True)

    op.create_table(
        'courses',
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_table(
        'users',
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('first_name', sa.String(length=100), nullable=False),
        sa.Column('last_name', sa.String(length=100), nullable=False),
        sa.Column('role', user_role_enum, nullable=False),
        sa.Column('status', user_status_enum, nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=False)

    op.create_table(
        'course_teacher_links',
        sa.Column('course_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['course_id'], ['courses.id']),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('course_id', 'user_id'),
    )

    op.create_table(
        'groups',
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('semester', sa.String(length=50), nullable=False),
        sa.Column('year', sa.Integer(), nullable=False),
        sa.Column('course_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['course_id'], ['courses.id']),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_table(
        'assignments',
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('language', sa.String(length=50), nullable=False),
        sa.Column('deadline', sa.DateTime(), nullable=True),
        sa.Column('max_score', sa.Integer(), nullable=False),
        sa.Column('reference_solution', sa.String(length=500), nullable=True),
        sa.Column('course_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['course_id'], ['courses.id']),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_table(
        'students',
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('full_name', sa.String(length=255), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=True),
        sa.Column('group_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['group_id'], ['groups.id']),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_table(
        'test_cases',
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('assignment_id', sa.Integer(), nullable=False),
        sa.Column('input_data', sa.Text(), nullable=False),
        sa.Column('expected_output', sa.Text(), nullable=False),
        sa.Column('weight', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['assignment_id'], ['assignments.id']),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_table(
        'submissions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('assignment_id', sa.Integer(), nullable=False),
        sa.Column('student_id', sa.Integer(), nullable=False),
        sa.Column('file_path', sa.String(length=500), nullable=False),
        sa.Column('submitted_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['assignment_id'], ['assignments.id']),
        sa.ForeignKeyConstraint(['student_id'], ['students.id']),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_table(
        'comments',
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('submission_id', sa.Integer(), nullable=False),
        sa.Column('author_id', sa.Integer(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('start_line_number', sa.Integer(), nullable=True),
        sa.Column('end_line_number', sa.Integer(), nullable=True),
        sa.Column('is_system_generated', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(['author_id'], ['users.id']),
        sa.ForeignKeyConstraint(['submission_id'], ['submissions.id']),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_table(
        'grades',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('submission_id', sa.Integer(), nullable=False),
        sa.Column('score', sa.Integer(), nullable=False),
        sa.Column('max_score', sa.Integer(), nullable=False),
        sa.Column('graded_by', sa.Integer(), nullable=False),
        sa.Column('graded_at', sa.DateTime(), nullable=False),
        sa.Column('is_published', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(['graded_by'], ['users.id']),
        sa.ForeignKeyConstraint(['submission_id'], ['submissions.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('submission_id'),
    )

    op.create_table(
        'plagiarism_reports',
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('submission_id', sa.Integer(), nullable=False),
        sa.Column('compared_with_id', sa.Integer(), nullable=False),
        sa.Column('similarity_percent', sa.Float(), nullable=False),
        sa.Column('detected_blocks', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['compared_with_id'], ['submissions.id']),
        sa.ForeignKeyConstraint(['submission_id'], ['submissions.id']),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_table(
        'test_results',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('submission_id', sa.Integer(), nullable=False),
        sa.Column('test_case_id', sa.Integer(), nullable=False),
        sa.Column('passed', sa.Boolean(), nullable=False),
        sa.Column('execution_time_ms', sa.Integer(), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['submission_id'], ['submissions.id']),
        sa.ForeignKeyConstraint(['test_case_id'], ['test_cases.id']),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade() -> None:
    op.drop_table('test_results')
    op.drop_table('plagiarism_reports')
    op.drop_table('grades')
    op.drop_table('comments')
    op.drop_table('submissions')
    op.drop_table('test_cases')
    op.drop_table('students')
    op.drop_table('assignments')
    op.drop_table('groups')
    op.drop_table('course_teacher_links')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_table('courses')

    bind = op.get_bind()
    user_status_enum.drop(bind, checkfirst=True)
    user_role_enum.drop(bind, checkfirst=True)
