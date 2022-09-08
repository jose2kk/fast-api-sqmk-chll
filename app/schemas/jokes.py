from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class JokesParamEnum(str, Enum):
    dad = "dad"
    chuck = "chuck"


class JokeCreateModel(BaseModel):
    text: str


class JokeModel(BaseModel):
    text: str
    number: int
    created_at: datetime
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]

    class Config:
        orm_mode = True


class JokeUpdateModel(BaseModel):
    text: str
