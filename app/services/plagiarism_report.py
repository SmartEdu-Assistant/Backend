from typing import Annotated

from fastapi import Depends

from app.models import (
    PlagiarismReport,
    PlagiarismReportCreate,
    PlagiarismReportUpdate,
)
from app.repositories import PlagiarismReportRepository
from app.services.base import BaseService


class PlagiarismReportService(
    BaseService[PlagiarismReport, PlagiarismReportCreate, PlagiarismReportUpdate]
):
    entity_name = 'PlagiarismReport'

    def __init__(
        self,
        repository: Annotated[
            PlagiarismReportRepository,
            Depends(PlagiarismReportRepository),
        ],
    ) -> None:
        super().__init__(repository)
