from fastapi import APIRouter, status

from app.dependencies.services import SubmissionServiceDep
from app.schemas import SubmissionCreate, SubmissionPublic, SubmissionUpdate


router = APIRouter(prefix='/submissions', tags=['submissions'])


@router.get('/', response_model=list[SubmissionPublic])
async def list_submissions(service: SubmissionServiceDep):
    return await service.list()


@router.get('/{submission_id}', response_model=SubmissionPublic)
async def get_submission(
    submission_id: int,
    service: SubmissionServiceDep,
):
    return await service.get(submission_id)


@router.post('/', response_model=SubmissionPublic, status_code=status.HTTP_201_CREATED)
async def create_submission(
    payload: SubmissionCreate,
    service: SubmissionServiceDep,
):
    return await service.create(payload)


@router.patch('/{submission_id}', response_model=SubmissionPublic)
async def update_submission(
    submission_id: int,
    payload: SubmissionUpdate,
    service: SubmissionServiceDep,
):
    return await service.update(submission_id, payload)


@router.delete('/{submission_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_submission(
    submission_id: int,
    service: SubmissionServiceDep,
):
    await service.delete(submission_id)
