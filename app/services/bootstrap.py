from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.rbac import build_role_scopes, collect_scope_set
from app.core.security import get_password_hash
from app.models import Permission, Role, User, UserStatus
from app.repositories import PermissionRepository, RoleRepository, UserRepository


class RBACBootstrapper:
    def __init__(self, session: AsyncSession) -> None:
        self.permission_repository = PermissionRepository(session)
        self.role_repository = RoleRepository(session)
        self.user_repository = UserRepository(session)

    async def bootstrap(self) -> None:
        permissions = await self._bootstrap_permissions()
        await self._bootstrap_roles(permissions)
        await self._bootstrap_admin_user()

    async def _bootstrap_permissions(self) -> dict[str, Permission]:
        role_scopes = build_role_scopes(
            public_role_name=settings.rbac.public_role_name,
            teacher_role_name=settings.rbac.teacher_role_name,
        )
        scope_set = collect_scope_set(role_scopes)
        permissions: dict[str, Permission] = {}

        for scope in sorted(scope_set):
            permission = await self.permission_repository.get_by_scope(scope)
            if permission is None:
                subject, action = scope.split(':', maxsplit=1)
                permission = await self.permission_repository.create(
                    {
                        'subject': subject,
                        'action': action,
                        'scope': scope,
                    },
                )
            permissions[scope] = permission

        return permissions

    async def _bootstrap_roles(self, permissions: dict[str, Permission]) -> None:
        role_scopes = build_role_scopes(
            public_role_name=settings.rbac.public_role_name,
            teacher_role_name=settings.rbac.teacher_role_name,
        )
        public_role = await self._upsert_role(
            settings.rbac.public_role_name,
            role_scopes.get(settings.rbac.public_role_name, []),
            permissions,
        )

        for role_name, scopes in role_scopes.items():
            if role_name == settings.rbac.public_role_name:
                continue
            await self._upsert_role(role_name, scopes, permissions)

        admin_role = await self.role_repository.get_by_name(settings.rbac.admin_role_name)
        if admin_role is None:
            admin_role = await self.role_repository.create(
                {'name': settings.rbac.admin_role_name},
            )

        admin_role.permissions = list(permissions.values())
        await self.role_repository.save(admin_role)

        if public_role.name == settings.rbac.admin_role_name:
            public_role.permissions = list(permissions.values())
            await self.role_repository.save(public_role)

    async def _bootstrap_admin_user(self) -> None:
        admin_user = await self.user_repository.get_by_email(settings.rbac.admin_email)
        admin_role = await self.role_repository.get_by_name(settings.rbac.admin_role_name)
        public_role = await self.role_repository.get_by_name(settings.rbac.public_role_name)
        desired_roles = [role for role in [admin_role, public_role] if role is not None]

        if admin_user is None:
            admin_user = User(
                email=settings.rbac.admin_email,
                first_name=settings.rbac.admin_first_name,
                last_name=settings.rbac.admin_last_name,
                status=UserStatus.ACTIVE,
                is_verified=True,
                password_hash=get_password_hash(settings.rbac.admin_password),
            )
            admin_user.roles = desired_roles
            await self.user_repository.save(admin_user)
            return

        existing_role_names = {role.name for role in admin_user.roles}
        for role in desired_roles:
            if role.name not in existing_role_names:
                admin_user.roles.append(role)
        admin_user.is_verified = True
        await self.user_repository.save(admin_user)

    async def _upsert_role(
        self,
        role_name: str,
        scopes: list[str],
        permissions: dict[str, Permission],
    ) -> Role:
        role = await self.role_repository.get_by_name(role_name)
        if role is None:
            role = await self.role_repository.create({'name': role_name})

        role.permissions = [permissions[scope] for scope in scopes if scope in permissions]
        return await self.role_repository.save(role)
