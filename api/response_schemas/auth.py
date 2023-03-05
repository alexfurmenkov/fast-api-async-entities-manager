from pydantic import BaseModel


class CreatedUserResponse(BaseModel):
    message: str
    user_id: str


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
