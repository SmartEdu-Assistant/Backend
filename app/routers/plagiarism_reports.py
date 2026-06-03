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
from app.dependencies.services import PlagiarismReportServiceDep
from app.schemas import (
    Page,
    PlagiarismReportCreate,
    PlagiarismReportPublic,
    PlagiarismReportUpdate,
)


router = APIRouter(
    prefix='/plagiarism-reports',
    tags=['plagiarism-reports'],
    responses=combine_responses(
        SERVER_ERROR_RESPONSES,
        VALIDATION_ERROR_RESPONSES,
        AUTH_ERROR_RESPONSES,
    ),
)


@router.get(
    '/',
    response_model=Page[PlagiarismReportPublic],
    dependencies=[Security(get_current_user, scopes=['plagiarism-reports:read'])],
)
async def list_plagiarism_reports(
    service: PlagiarismReportServiceDep,
    pagination: PaginationDep,
):
    return await service.list(pagination)


@router.get(
    '/{report_id}',
    response_model=PlagiarismReportPublic,
    dependencies=[Security(get_current_user, scopes=['plagiarism-reports:read'])],
    responses=NOT_FOUND_ERROR_RESPONSES,
)
async def get_plagiarism_report(report_id: int, service: PlagiarismReportServiceDep):
    return await service.get(report_id)


@router.post(
    '/',
    response_model=PlagiarismReportPublic,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Security(get_current_user, scopes=['plagiarism-reports:write'])],
)
async def create_plagiarism_report(
    payload: PlagiarismReportCreate,
    service: PlagiarismReportServiceDep,
):
    return await service.create(payload)


@router.patch(
    '/{report_id}',
    response_model=PlagiarismReportPublic,
    dependencies=[Security(get_current_user, scopes=['plagiarism-reports:write'])],
    responses=NOT_FOUND_ERROR_RESPONSES,
)
async def update_plagiarism_report(
    report_id: int,
    payload: PlagiarismReportUpdate,
    service: PlagiarismReportServiceDep,
):
    return await service.update(report_id, payload)


@router.delete(
    '/{report_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Security(get_current_user, scopes=['plagiarism-reports:write'])],
    responses=NOT_FOUND_ERROR_RESPONSES,
)
async def delete_plagiarism_report(
    report_id: int,
    service: PlagiarismReportServiceDep,
):
    await service.delete(report_id)
