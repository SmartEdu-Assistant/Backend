from typing import Annotated

from fastapi import Depends

from app.models import Group, GroupCreate, GroupUpdate
from app.repositories import GroupRepository
from app.services.base import BaseService


class GroupService(BaseService[Group, GroupCreate, GroupUpdate]):
    entity_name = 'Group'

    def __init__(
        self,
        repository: Annotated[GroupRepository, Depends(GroupRepository)],
    ) -> None:
        super().__init__(repository)
