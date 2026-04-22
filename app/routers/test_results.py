from fastapi import APIRouter, Depends, status

from app.dependencies.services import get_test_result_service
from app.schemas import TestResultCreate, TestResultPublic, TestResultUpdate
from app.services import TestResultService


router = APIRouter(prefix='/test-results', tags=['test-results'])


@router.get('/', response_model=list[TestResultPublic])
async def list_test_results(service: TestResultService = Depends(get_test_result_service)):
    return await service.list()


@router.get('/{test_result_id}', response_model=TestResultPublic)
async def get_test_result(
    test_result_id: int,
    service: TestResultService = Depends(get_test_result_service),
):
    return await service.get(test_result_id)


@router.post('/', response_model=TestResultPublic, status_code=status.HTTP_201_CREATED)
async def create_test_result(
    payload: TestResultCreate,
    service: TestResultService = Depends(get_test_result_service),
):
    return await service.create(payload)


@router.patch('/{test_result_id}', response_model=TestResultPublic)
async def update_test_result(
    test_result_id: int,
    payload: TestResultUpdate,
    service: TestResultService = Depends(get_test_result_service),
):
    return await service.update(test_result_id, payload)


@router.delete('/{test_result_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_test_result(
    test_result_id: int,
    service: TestResultService = Depends(get_test_result_service),
):
    await service.delete(test_result_id)
