from collections.abc import Sequence


SCOPE_DESCRIPTIONS = {
    'profile:read': 'Read current user profile',
    'users:read': 'Read users',
    'users:write': 'Manage users and roles',
    'courses:read': 'Read courses',
    'courses:write': 'Manage courses',
    'groups:read': 'Read groups',
    'groups:write': 'Manage groups',
    'students:read': 'Read students',
    'students:write': 'Manage students',
    'assignments:read': 'Read assignments',
    'assignments:write': 'Manage assignments',
    'submissions:read': 'Read submissions',
    'submissions:write': 'Manage submissions',
    'comments:read': 'Read comments',
    'comments:write': 'Manage comments',
    'grades:read': 'Read grades',
    'grades:write': 'Manage grades',
    'test-cases:read': 'Read test cases',
    'test-cases:write': 'Manage test cases',
    'test-results:read': 'Read test results',
    'test-results:write': 'Manage test results',
    'plagiarism-reports:read': 'Read plagiarism reports',
    'plagiarism-reports:write': 'Manage plagiarism reports',
}

TEACHER_SCOPES = [
    'profile:read',
    'users:read',
    'courses:read',
    'courses:write',
    'groups:read',
    'groups:write',
    'students:read',
    'students:write',
    'assignments:read',
    'assignments:write',
    'submissions:read',
    'submissions:write',
    'comments:read',
    'comments:write',
    'grades:read',
    'grades:write',
    'test-cases:read',
    'test-cases:write',
    'test-results:read',
    'test-results:write',
    'plagiarism-reports:read',
    'plagiarism-reports:write',
]


def build_role_scopes(
    *,
    public_role_name: str,
    teacher_role_name: str,
) -> dict[str, list[str]]:
    return {
        public_role_name: ['profile:read'],
        teacher_role_name: list(TEACHER_SCOPES),
    }


def collect_scope_set(role_scopes: dict[str, Sequence[str]]) -> set[str]:
    return {
        scope
        for scopes in role_scopes.values()
        for scope in scopes
    }
