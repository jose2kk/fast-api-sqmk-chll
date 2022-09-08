from datetime import datetime
from typing import Optional

from app.database.models.joke import Joke
from app.schemas.jokes import (
    JokeCreateModel,
    JokeModel,
    JokeUpdateModel,
)


def create_joke(joke: JokeCreateModel) -> JokeModel:
    joke_create = Joke(
        text=joke.text,
        created_at=datetime.utcnow(),
    )
    joke_from_db = joke_create.save()
    return JokeModel.from_orm(joke_from_db)


def _get_joke_by_number(number: int) -> Optional["Joke"]:
    joke_from_db = Joke.get_by_number(number=number)
    if joke_from_db and joke_from_db.deleted_at:
        return None
    return joke_from_db


def update_joke(number: int, joke: JokeUpdateModel) -> Optional[JokeModel]:
    joke_from_db = _get_joke_by_number(number=number)
    if not joke_from_db:
        return None
    joke_from_db.update(text=joke.text)
    return JokeModel.from_orm(joke_from_db)


def delete_joke(number: int) -> Optional[JokeModel]:
    joke_from_db = _get_joke_by_number(number=number)
    if joke_from_db and joke_from_db.deleted_at is None:
        joke_from_db.delete()
        return JokeModel.from_orm(joke_from_db)
    return None
