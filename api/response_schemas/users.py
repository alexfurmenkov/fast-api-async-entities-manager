from pydantic import BaseModel


class UserInfo(BaseModel):
    id: str
    username: str
    name: str
    surname: str
    age: str | None = None

    class Config:
        orm_mode = True


class UpdatedUserResponse(BaseModel):
    message: str
    user_id: str


class DeletedUserResponse(BaseModel):
    message: str
    user_id: str
