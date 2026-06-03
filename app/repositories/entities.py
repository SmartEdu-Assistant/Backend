from datetime import datetime, timezone

from sqlalchemy.orm import selectinload
from sqlmodel import select

from app.models import (
    Assignment,
    Comment,
    Course,
    Grade,
    Group,
    Permission,
    PlagiarismReport,
    RefreshSession,
    Role,
    Student,
    Submission,
    TestCase,
    TestResult,
    User,
)
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    model = User

    async def list(self) -> list[User]:
        result = await self.session.exec(
            select(User).options(selectinload(User.roles)),
        )
        return list(result.all())

    async def get(self, entity_id: int) -> User | None:
        result = await self.session.exec(
            select(User)
            .where(User.id == entity_id)
            .options(selectinload(User.roles).selectinload(Role.permissions)),
        )
        return result.first()

    async def get_by_email(self, email: str) -> User | None:
        result = await self.session.exec(
            select(User)
            .where(User.email == email)
            .options(selectinload(User.roles).selectinload(Role.permissions)),
        )
        return result.first()


class RoleRepository(BaseRepository[Role]):
    model = Role

    async def get_by_name(self, name: str) -> Role | None:
        result = await self.session.exec(
            select(Role)
            .where(Role.name == name)
            .options(selectinload(Role.permissions)),
        )
        return result.first()

    async def get_by_names(self, names: list[str]) -> list[Role]:
        if not names:
            return []

        result = await self.session.exec(
            select(Role)
            .where(Role.name.in_(names))
            .options(selectinload(Role.permissions)),
        )
        return list(result.all())


class PermissionRepository(BaseRepository[Permission]):
    model = Permission

    async def get_by_scope(self, scope: str) -> Permission | None:
        result = await self.session.exec(
            select(Permission).where(Permission.scope == scope),
        )
        return result.first()

    async def get_by_scopes(self, scopes: list[str]) -> list[Permission]:
        if not scopes:
            return []

        result = await self.session.exec(
            select(Permission).where(Permission.scope.in_(scopes)),
        )
        return list(result.all())


class RefreshSessionRepository(BaseRepository[RefreshSession]):
    model = RefreshSession

    async def get_active_by_jti(self, jti: str) -> RefreshSession | None:
        now = datetime.now(timezone.utc)
        result = await self.session.exec(
            select(RefreshSession)
            .where(RefreshSession.jti == jti)
            .where(RefreshSession.revoked_at.is_(None))
            .where(RefreshSession.expires_at > now),
        )
        return result.first()

    async def revoke(self, refresh_session: RefreshSession) -> RefreshSession:
        refresh_session.revoked_at = datetime.now(timezone.utc)
        return await self.save(refresh_session)

    async def revoke_for_user(self, user_id: int) -> None:
        now = datetime.now(timezone.utc)
        result = await self.session.exec(
            select(RefreshSession)
            .where(RefreshSession.user_id == user_id)
            .where(RefreshSession.revoked_at.is_(None)),
        )
        for session in result.all():
            session.revoked_at = now
            self.session.add(session)
        await self.session.commit()


class CourseRepository(BaseRepository[Course]):
    model = Course


class GroupRepository(BaseRepository[Group]):
    model = Group


class StudentRepository(BaseRepository[Student]):
    model = Student


class AssignmentRepository(BaseRepository[Assignment]):
    model = Assignment


class TestCaseRepository(BaseRepository[TestCase]):
    model = TestCase


class SubmissionRepository(BaseRepository[Submission]):
    model = Submission


class TestResultRepository(BaseRepository[TestResult]):
    model = TestResult


class CommentRepository(BaseRepository[Comment]):
    model = Comment


class GradeRepository(BaseRepository[Grade]):
    model = Grade


class PlagiarismReportRepository(BaseRepository[PlagiarismReport]):
    model = PlagiarismReport
