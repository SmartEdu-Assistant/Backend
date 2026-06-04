"""sync timestamp columns with current models

Revision ID: c42507c304eb
Revises: 20260531_0003
Create Date: 2026-06-03 14:28:33.235371
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = 'c42507c304eb'
down_revision = '20260531_0003'
branch_labels = None
depends_on = None


def _add_updated_at(table_name: str) -> None:
    op.add_column(
        table_name,
        sa.Column(
            'updated_at',
            sa.DateTime(),
            nullable=False,
            server_default=sa.text('NOW()'),
        ),
    )
    op.alter_column(table_name, 'updated_at', server_default=None)


def upgrade() -> None:
    for table_name in (
        'assignments',
        'comments',
        'courses',
        'groups',
        'plagiarism_reports',
        'students',
        'test_cases',
        'users',
    ):
        _add_updated_at(table_name)

    op.add_column(
        'grades',
        sa.Column(
            'created_at',
            sa.DateTime(),
            nullable=False,
            server_default=sa.text('NOW()'),
        ),
    )
    op.add_column(
        'grades',
        sa.Column(
            'updated_at',
            sa.DateTime(),
            nullable=False,
            server_default=sa.text('NOW()'),
        ),
    )
    op.execute("UPDATE grades SET created_at = graded_at, updated_at = graded_at")
    op.alter_column('grades', 'created_at', server_default=None)
    op.alter_column('grades', 'updated_at', server_default=None)
    op.drop_column('grades', 'graded_at')

    op.add_column(
        'submissions',
        sa.Column(
            'created_at',
            sa.DateTime(),
            nullable=False,
            server_default=sa.text('NOW()'),
        ),
    )
    op.add_column(
        'submissions',
        sa.Column(
            'updated_at',
            sa.DateTime(),
            nullable=False,
            server_default=sa.text('NOW()'),
        ),
    )
    op.execute(
        "UPDATE submissions SET created_at = submitted_at, updated_at = submitted_at",
    )
    op.alter_column('submissions', 'created_at', server_default=None)
    op.alter_column('submissions', 'updated_at', server_default=None)
    op.drop_column('submissions', 'submitted_at')


def downgrade() -> None:
    op.add_column(
        'submissions',
        sa.Column(
            'submitted_at',
            sa.DateTime(),
            nullable=False,
            server_default=sa.text('NOW()'),
        ),
    )
    op.execute("UPDATE submissions SET submitted_at = created_at")
    op.alter_column('submissions', 'submitted_at', server_default=None)
    op.drop_column('submissions', 'updated_at')
    op.drop_column('submissions', 'created_at')

    op.add_column(
        'grades',
        sa.Column(
            'graded_at',
            sa.DateTime(),
            nullable=False,
            server_default=sa.text('NOW()'),
        ),
    )
    op.execute("UPDATE grades SET graded_at = created_at")
    op.alter_column('grades', 'graded_at', server_default=None)
    op.drop_column('grades', 'updated_at')
    op.drop_column('grades', 'created_at')

    for table_name in (
        'users',
        'test_cases',
        'students',
        'plagiarism_reports',
        'groups',
        'courses',
        'comments',
        'assignments',
    ):
        op.drop_column(table_name, 'updated_at')
