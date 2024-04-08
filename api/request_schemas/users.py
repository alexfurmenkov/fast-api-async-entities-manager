from typing import Optional

from pydantic import BaseModel, model_validator


class CreateUserRequestSchema(BaseModel):
    username: str
    password: str
    name: str
    surname: str
    age: Optional[int]


class UpdateUserRequestSchema(BaseModel):
    username: Optional[str]
    name: Optional[str]
    surname: Optional[str]
    age: Optional[int]

    @model_validator(mode="before")
    def any_of(cls, values: dict):
        if not any(values.values()):
            raise ValueError("one of username, name, surname or age must have a value")
        return {k: v for k, v in values.items() if v is not None}
