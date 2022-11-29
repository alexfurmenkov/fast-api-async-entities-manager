from pydantic import BaseModel


class User(BaseModel):
    id: str
    username: str
    name: str
    surname: str
    age: int
