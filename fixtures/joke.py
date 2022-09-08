from datetime import datetime

import pytest

from app.schemas.jokes import JokeModel


def build_joke_model(**kwargs) -> JokeModel:
    params = dict(
        text="this is a nice joke!",
        number=1,
        created_at=datetime.utcnow(),
    )

    params.update(kwargs)
    return JokeModel.parse_obj(params)


@pytest.fixture
def joke_model() -> JokeModel:
    return build_joke_model()
