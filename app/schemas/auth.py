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
    message: str = 'Operation completed successfully'


class ConfirmAccountRequest(SQLModel):
    token: str


class ChangePasswordRequest(SQLModel):
    current_password: str
    new_password: str

