"""add email notifications and account verification

Revision ID: 20260531_0003
Revises: 20260526_0002
Create Date: 2026-05-31 00:00:00
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = '20260531_0003'
down_revision = '20260526_0002'
branch_labels = None
depends_on = None


email_notification_status_enum = postgresql.ENUM(
    'PENDING',
    'SENT',
    'FAILED',
    name='emailnotificationstatus',
    create_type=False,
)


def upgrade() -> None:
    bind = op.get_bind()
    email_notification_status_enum.create(bind, checkfirst=True)

    op.add_column(
        'users',
        sa.Column('is_verified', sa.Boolean(), nullable=False, server_default=sa.false()),
    )

    op.create_table(
        'email_notifications',
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('recipient', sa.String(length=255), nullable=False),
        sa.Column('subject', sa.String(length=255), nullable=False),
        sa.Column('template_name', sa.String(length=255), nullable=False),
        sa.Column('body', sa.Text(), nullable=False),
        sa.Column('status', email_notification_status_enum, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('sent_at', sa.DateTime(), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('confirmation_token', sa.String(length=255), nullable=True),
        sa.Column('confirmation_token_expires_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(
        op.f('ix_email_notifications_confirmation_token'),
        'email_notifications',
        ['confirmation_token'],
        unique=True,
    )

    op.alter_column('users', 'is_verified', server_default=None)


def downgrade() -> None:
    op.drop_index(
        op.f('ix_email_notifications_confirmation_token'),
        table_name='email_notifications',
    )
    op.drop_table('email_notifications')
    op.drop_column('users', 'is_verified')

    bind = op.get_bind()
    email_notification_status_enum.drop(bind, checkfirst=True)
