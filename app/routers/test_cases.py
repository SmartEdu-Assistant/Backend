from fastapi import APIRouter, Depends, status

from app.dependencies.services import get_test_case_service
from app.schemas import TestCaseCreate, TestCasePublic, TestCaseUpdate
from app.services import TestCaseService


router = APIRouter(prefix='/test-cases', tags=['test-cases'])


@router.get('/', response_model=list[TestCasePublic])
async def list_test_cases(service: TestCaseService = Depends(get_test_case_service)):
    return await service.list()


@router.get('/{test_case_id}', response_model=TestCasePublic)
async def get_test_case(
    test_case_id: int,
    service: TestCaseService = Depends(get_test_case_service),
):
    return await service.get(test_case_id)


@router.post('/', response_model=TestCasePublic, status_code=status.HTTP_201_CREATED)
async def create_test_case(
    payload: TestCaseCreate,
    service: TestCaseService = Depends(get_test_case_service),
):
    return await service.create(payload)


@router.patch('/{test_case_id}', response_model=TestCasePublic)
async def update_test_case(
    test_case_id: int,
    payload: TestCaseUpdate,
    service: TestCaseService = Depends(get_test_case_service),
):
    return await service.update(test_case_id, payload)


@router.delete('/{test_case_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_test_case(
    test_case_id: int,
    service: TestCaseService = Depends(get_test_case_service),
):
    await service.delete(test_case_id)
