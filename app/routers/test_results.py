from fastapi import APIRouter, Security, status

from app.core.api_docs import (
    AUTH_ERROR_RESPONSES,
    NOT_FOUND_ERROR_RESPONSES,
    SERVER_ERROR_RESPONSES,
    VALIDATION_ERROR_RESPONSES,
    combine_responses,
)
from app.dependencies.auth import get_current_user
from app.dependencies.pagination import PaginationDep
from app.dependencies.services import TestResultServiceDep
from app.schemas import Page, TestResultCreate, TestResultPublic, TestResultUpdate


router = APIRouter(
    prefix='/test-results',
    tags=['test-results'],
    responses=combine_responses(
        SERVER_ERROR_RESPONSES,
        VALIDATION_ERROR_RESPONSES,
        AUTH_ERROR_RESPONSES,
    ),
)


@router.get(
    '/',
    response_model=Page[TestResultPublic],
    dependencies=[Security(get_current_user, scopes=['test-results:read'])],
)
async def list_test_results(service: TestResultServiceDep, pagination: PaginationDep):
    return await service.list(pagination)


@router.get(
    '/{test_result_id}',
    response_model=TestResultPublic,
    dependencies=[Security(get_current_user, scopes=['test-results:read'])],
    responses=NOT_FOUND_ERROR_RESPONSES,
)
async def get_test_result(test_result_id: int, service: TestResultServiceDep):
    return await service.get(test_result_id)


@router.post(
    '/',
    response_model=TestResultPublic,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Security(get_current_user, scopes=['test-results:write'])],
)
async def create_test_result(
    payload: TestResultCreate,
    service: TestResultServiceDep,
):
    return await service.create(payload)


@router.patch(
    '/{test_result_id}',
    response_model=TestResultPublic,
    dependencies=[Security(get_current_user, scopes=['test-results:write'])],
    responses=NOT_FOUND_ERROR_RESPONSES,
)
async def update_test_result(
    test_result_id: int,
    payload: TestResultUpdate,
    service: TestResultServiceDep,
):
    return await service.update(test_result_id, payload)


@router.delete(
    '/{test_result_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Security(get_current_user, scopes=['test-results:write'])],
    responses=NOT_FOUND_ERROR_RESPONSES,
)
async def delete_test_result(test_result_id: int, service: TestResultServiceDep):
    await service.delete(test_result_id)
