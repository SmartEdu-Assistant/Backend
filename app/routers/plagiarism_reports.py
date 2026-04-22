from fastapi import APIRouter, Depends, status

from app.dependencies.services import get_plagiarism_report_service
from app.schemas import PlagiarismReportCreate, PlagiarismReportPublic, PlagiarismReportUpdate
from app.services import PlagiarismReportService


router = APIRouter(prefix='/plagiarism-reports', tags=['plagiarism-reports'])


@router.get('/', response_model=list[PlagiarismReportPublic])
async def list_plagiarism_reports(
    service: PlagiarismReportService = Depends(get_plagiarism_report_service),
):
    return await service.list()


@router.get('/{report_id}', response_model=PlagiarismReportPublic)
async def get_plagiarism_report(
    report_id: int,
    service: PlagiarismReportService = Depends(get_plagiarism_report_service),
):
    return await service.get(report_id)


@router.post('/', response_model=PlagiarismReportPublic, status_code=status.HTTP_201_CREATED)
async def create_plagiarism_report(
    payload: PlagiarismReportCreate,
    service: PlagiarismReportService = Depends(get_plagiarism_report_service),
):
    return await service.create(payload)


@router.patch('/{report_id}', response_model=PlagiarismReportPublic)
async def update_plagiarism_report(
    report_id: int,
    payload: PlagiarismReportUpdate,
    service: PlagiarismReportService = Depends(get_plagiarism_report_service),
):
    return await service.update(report_id, payload)


@router.delete('/{report_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_plagiarism_report(
    report_id: int,
    service: PlagiarismReportService = Depends(get_plagiarism_report_service),
):
    await service.delete(report_id)
