from fastapi import APIRouter, Security, status

from app.dependencies.auth import get_current_user
from app.dependencies.services import TestCaseServiceDep
from app.schemas import TestCaseCreate, TestCasePublic, TestCaseUpdate


router = APIRouter(prefix='/test-cases', tags=['test-cases'])


@router.get(
    '/',
    response_model=list[TestCasePublic],
    dependencies=[Security(get_current_user, scopes=['test-cases:read'])],
)
async def list_test_cases(service: TestCaseServiceDep):
    return await service.list()


@router.get(
    '/{test_case_id}',
    response_model=TestCasePublic,
    dependencies=[Security(get_current_user, scopes=['test-cases:read'])],
)
async def get_test_case(test_case_id: int, service: TestCaseServiceDep):
    return await service.get(test_case_id)


@router.post(
    '/',
    response_model=TestCasePublic,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Security(get_current_user, scopes=['test-cases:write'])],
)
async def create_test_case(
    payload: TestCaseCreate,
    service: TestCaseServiceDep,
):
    return await service.create(payload)


@router.patch(
    '/{test_case_id}',
    response_model=TestCasePublic,
    dependencies=[Security(get_current_user, scopes=['test-cases:write'])],
)
async def update_test_case(
    test_case_id: int,
    payload: TestCaseUpdate,
    service: TestCaseServiceDep,
):
    return await service.update(test_case_id, payload)


@router.delete(
    '/{test_case_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Security(get_current_user, scopes=['test-cases:write'])],
)
async def delete_test_case(test_case_id: int, service: TestCaseServiceDep):
    await service.delete(test_case_id)
