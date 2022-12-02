from typing import Optional

from pydantic import BaseModel


class UserRequestSchema(BaseModel):
    username: str
    name: str
    surname: str
    age: Optional[int]
