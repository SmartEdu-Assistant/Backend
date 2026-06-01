"""add auth and rbac

Revision ID: 20260526_0002
Revises: 20260407_0001
Create Date: 2026-05-26 00:00:00
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = '20260526_0002'
down_revision = '20260407_0001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'permissions',
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('subject', sa.String(length=100), nullable=False),
        sa.Column('action', sa.String(length=100), nullable=False),
        sa.Column('scope', sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('scope'),
    )
    op.create_index(op.f('ix_permissions_scope'), 'permissions', ['scope'], unique=True)

    op.create_table(
        'roles',
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name'),
    )
    op.create_index(op.f('ix_roles_name'), 'roles', ['name'], unique=True)

    op.create_table(
        'role_permission_links',
        sa.Column('role_id', sa.Integer(), nullable=False),
        sa.Column('permission_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['permission_id'], ['permissions.id']),
        sa.ForeignKeyConstraint(['role_id'], ['roles.id']),
        sa.PrimaryKeyConstraint('role_id', 'permission_id'),
    )

    op.create_table(
        'user_role_links',
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('role_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['role_id'], ['roles.id']),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('user_id', 'role_id'),
    )

    op.create_table(
        'refresh_sessions',
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('jti', sa.String(length=255), nullable=False),
        sa.Column('expires_at', sa.DateTime(), nullable=False),
        sa.Column('revoked_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('jti'),
    )
    op.create_index(op.f('ix_refresh_sessions_jti'), 'refresh_sessions', ['jti'], unique=True)
    op.create_index(op.f('ix_refresh_sessions_user_id'), 'refresh_sessions', ['user_id'], unique=False)

    op.execute(
        """
        INSERT INTO roles (created_at, updated_at, name)
        VALUES
            (NOW(), NOW(), 'admin'),
            (NOW(), NOW(), 'teacher'),
            (NOW(), NOW(), 'public')
        ON CONFLICT (name) DO NOTHING
        """,
    )
    op.execute(
        """
        INSERT INTO user_role_links (user_id, role_id)
        SELECT users.id, roles.id
        FROM users
        JOIN roles ON roles.name = CASE
            WHEN users.role = 'ADMIN' THEN 'admin'
            ELSE 'teacher'
        END
        ON CONFLICT DO NOTHING
        """,
    )
    op.execute(
        """
        INSERT INTO user_role_links (user_id, role_id)
        SELECT users.id, roles.id
        FROM users
        JOIN roles ON roles.name = 'public'
        ON CONFLICT DO NOTHING
        """,
    )

    op.drop_column('users', 'role')
    op.execute("DROP TYPE IF EXISTS userrole")


def downgrade() -> None:
    op.add_column(
        'users',
        sa.Column(
            'role',
            sa.String(length=50),
            nullable=False,
            server_default='TEACHER',
        ),
    )
    op.execute(
        """
        UPDATE users
        SET role = CASE
            WHEN EXISTS (
                SELECT 1
                FROM user_role_links url
                JOIN roles r ON r.id = url.role_id
                WHERE url.user_id = users.id AND r.name = 'admin'
            ) THEN 'ADMIN'
            ELSE 'TEACHER'
        END
        """,
    )
    op.alter_column('users', 'role', server_default=None)

    op.drop_index(op.f('ix_refresh_sessions_user_id'), table_name='refresh_sessions')
    op.drop_index(op.f('ix_refresh_sessions_jti'), table_name='refresh_sessions')
    op.drop_table('refresh_sessions')
    op.drop_table('user_role_links')
    op.drop_table('role_permission_links')
    op.drop_index(op.f('ix_roles_name'), table_name='roles')
    op.drop_table('roles')
    op.drop_index(op.f('ix_permissions_scope'), table_name='permissions')
    op.drop_table('permissions')
