from fastapi import APIRouter

from app.core.config import settings
from app.routers.assignments import router as assignments_router
from app.routers.comments import router as comments_router
from app.routers.courses import router as courses_router
from app.routers.grades import router as grades_router
from app.routers.groups import router as groups_router
from app.routers.plagiarism_reports import router as plagiarism_reports_router
from app.routers.students import router as students_router
from app.routers.submissions import router as submissions_router
from app.routers.test_cases import router as test_cases_router
from app.routers.test_results import router as test_results_router
from app.routers.users import router as users_router


api_router = APIRouter(prefix=settings.api_v1_prefix)
api_router.include_router(users_router)
api_router.include_router(courses_router)
api_router.include_router(groups_router)
api_router.include_router(students_router)
api_router.include_router(assignments_router)
api_router.include_router(test_cases_router)
api_router.include_router(submissions_router)
api_router.include_router(test_results_router)
api_router.include_router(comments_router)
api_router.include_router(grades_router)
api_router.include_router(plagiarism_reports_router)
