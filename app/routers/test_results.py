from fastapi import APIRouter, status

from app.dependencies.services import TestResultServiceDep
from app.schemas import TestResultCreate, TestResultPublic, TestResultUpdate


router = APIRouter(prefix='/test-results', tags=['test-results'])


@router.get('/', response_model=list[TestResultPublic])
async def list_test_results(service: TestResultServiceDep):
    return await service.list()


@router.get('/{test_result_id}', response_model=TestResultPublic)
async def get_test_result(
    test_result_id: int,
    service: TestResultServiceDep,
):
    return await service.get(test_result_id)


@router.post('/', response_model=TestResultPublic, status_code=status.HTTP_201_CREATED)
async def create_test_result(
    payload: TestResultCreate,
    service: TestResultServiceDep,
):
    return await service.create(payload)


@router.patch('/{test_result_id}', response_model=TestResultPublic)
async def update_test_result(
    test_result_id: int,
    payload: TestResultUpdate,
    service: TestResultServiceDep,
):
    return await service.update(test_result_id, payload)


@router.delete('/{test_result_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_test_result(
    test_result_id: int,
    service: TestResultServiceDep,
):
    await service.delete(test_result_id)
