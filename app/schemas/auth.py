from sqlmodel import SQLModel


class LoginRequest(SQLModel):
    email: str
    password: str


class TokenPair(SQLModel):
    access_token: str
    refresh_token: str
    token_type: str = 'bearer'


class AuthSuccessResponse(SQLModel):
    success: bool = True

