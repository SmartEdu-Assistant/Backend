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
from app.dependencies.services import SubmissionServiceDep
from app.schemas import Page, SubmissionCreate, SubmissionPublic, SubmissionUpdate


router = APIRouter(
    prefix='/submissions',
    tags=['submissions'],
    responses=combine_responses(
        SERVER_ERROR_RESPONSES,
        VALIDATION_ERROR_RESPONSES,
        AUTH_ERROR_RESPONSES,
    ),
)


@router.get(
    '/',
    response_model=Page[SubmissionPublic],
    dependencies=[Security(get_current_user, scopes=['submissions:read'])],
)
async def list_submissions(service: SubmissionServiceDep, pagination: PaginationDep):
    return await service.list(pagination)


@router.get(
    '/{submission_id}',
    response_model=SubmissionPublic,
    dependencies=[Security(get_current_user, scopes=['submissions:read'])],
    responses=NOT_FOUND_ERROR_RESPONSES,
)
async def get_submission(submission_id: int, service: SubmissionServiceDep):
    return await service.get(submission_id)


@router.post(
    '/',
    response_model=SubmissionPublic,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Security(get_current_user, scopes=['submissions:write'])],
)
async def create_submission(
    payload: SubmissionCreate,
    service: SubmissionServiceDep,
):
    return await service.create(payload)


@router.patch(
    '/{submission_id}',
    response_model=SubmissionPublic,
    dependencies=[Security(get_current_user, scopes=['submissions:write'])],
    responses=NOT_FOUND_ERROR_RESPONSES,
)
async def update_submission(
    submission_id: int,
    payload: SubmissionUpdate,
    service: SubmissionServiceDep,
):
    return await service.update(submission_id, payload)


@router.delete(
    '/{submission_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Security(get_current_user, scopes=['submissions:write'])],
    responses=NOT_FOUND_ERROR_RESPONSES,
)
async def delete_submission(submission_id: int, service: SubmissionServiceDep):
    await service.delete(submission_id)
