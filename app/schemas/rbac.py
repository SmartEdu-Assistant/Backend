from sqlmodel import SQLModel


class UpdateUserRolesRequest(SQLModel):
    role_names: list[str]
