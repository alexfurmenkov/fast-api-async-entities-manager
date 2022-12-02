from pydantic import BaseModel


class UserRequestSchema(BaseModel):
    id: str
    username: str
    name: str
    surname: str
    age: int