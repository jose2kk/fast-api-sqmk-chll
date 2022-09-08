from datetime import datetime
import json
from unittest.mock import (
    MagicMock,
    Mock,
)

import pytest
from fastapi.testclient import TestClient

from app.schemas.jokes import (
    JokeModel,
    JokeCreateModel,
    JokeUpdateModel,
)
from app.services.jokes import service as jokes_service
from fixtures.client import test_client
from fixtures.joke import joke_model


@pytest.fixture
def mock_random(mocker) -> Mock:
    return mocker.patch('app.main.random', autospec=True, spec_set=True)


@pytest.fixture
def mock_jokes_service(mocker) -> Mock:
    return mocker.patch('app.main.jokes_service', autospec=True, spec_set=True)


@pytest.fixture
def mock_jokes_db(mocker) -> Mock:
    return mocker.patch('app.main.jokes_db', autospec=True, spec_set=True)


@pytest.fixture
def return_joke() -> str:
    return "goodjoke"


def test_get_jokes_endpoint__no_path_param(
    test_client: TestClient,
    mock_random: Mock,
):
    mock_random.choice = MagicMock()
    mock_random.choice.return_value = jokes_service.get_chuck_norris_joke

    resp = test_client.get("/v1/jokes/")

    assert resp.json() is not None
    assert resp.status_code == 200

    mock_random.choice.assert_called_once()


def test_get_jokes_endpoint__path_param__dad(
    return_joke: str,
    test_client: TestClient,
    mock_jokes_service: Mock,
    mock_random: Mock,
):
    mock_random.choice = MagicMock()

    mock_jokes_service.get_dad_joke = MagicMock()
    mock_jokes_service.get_dad_joke.return_value = return_joke

    mock_jokes_service.get_chuck_norris_joke = MagicMock()

    resp = test_client.get("/v1/jokes/dad")

    assert resp.json() == {"result": return_joke}
    assert resp.status_code == 200

    mock_random.choice.assert_not_called()
    mock_jokes_service.get_chuck_norris_joke.assert_not_called()
    mock_jokes_service.get_dad_joke.assert_called_once()


def test_get_jokes_endpoint__path_param__chuck(
    return_joke: str,
    test_client: TestClient,
    mock_jokes_service: Mock,
    mock_random: Mock,
):
    mock_random.choice = MagicMock()

    mock_jokes_service.get_chuck_norris_joke = MagicMock()
    mock_jokes_service.get_chuck_norris_joke.return_value = return_joke

    mock_jokes_service.get_dad_joke = MagicMock()

    resp = test_client.get("/v1/jokes/chuck")

    assert resp.json() == {"result": return_joke}
    assert resp.status_code == 200

    mock_random.choice.assert_not_called()
    mock_jokes_service.get_chuck_norris_joke.assert_called_once()
    mock_jokes_service.get_dad_joke.assert_not_called()


def test_get_jokes_endpoint__unexpected_path_param(
    test_client: TestClient,
    mock_jokes_service: Mock,
    mock_random: Mock,
):
    mock_random.choice = MagicMock()

    mock_jokes_service.get_chuck_norris_joke = MagicMock()

    mock_jokes_service.get_dad_joke = MagicMock()

    resp = test_client.get("/v1/jokes/somethingwrong")

    assert resp.status_code == 422

    mock_random.choice.assert_not_called()
    mock_jokes_service.get_chuck_norris_joke.assert_not_called()
    mock_jokes_service.get_dad_joke.assert_not_called()

from app.logger import logger

def test_post_jokes_endpoint(
    joke_model: JokeModel,
    test_client: TestClient,
    mock_jokes_db: Mock,
):
    joke_create_model = JokeCreateModel(text=joke_model.text)

    mock_jokes_db.create_joke = MagicMock()
    mock_jokes_db.create_joke.return_value = joke_model 

    resp = test_client.post("/v1/jokes/", json=joke_create_model.dict(exclude_unset=True))

    assert resp.json() == {
        "result": "joke created",
        "created": json.loads(joke_model.json(exclude_unset=True)),
    }
    assert resp.status_code == 201

    mock_jokes_db.create_joke.assert_called_once_with(joke=joke_create_model)


def test_update_jokes_endpoint(
    joke_model: JokeModel,
    test_client: TestClient,
    mock_jokes_db: Mock,
):
    joke_update = JokeUpdateModel(text="updated joke!")

    mock_jokes_db.update_joke = MagicMock()
    mock_jokes_db.update_joke.return_value = joke_model

    resp = test_client.patch(
        f"/v1/jokes/{joke_model.number}",
        json=joke_update.dict(exclude_unset=True),
    )

    assert resp.json()["result"] == "updated"
    assert JokeModel(**resp.json().get("updated"))
    assert resp.status_code == 200

    mock_jokes_db.update_joke.assert_called_once_with(
        number=joke_model.number, joke=joke_update
    )


def test_update_jokes_endpoint__deleted(
    joke_model: JokeModel,
    test_client: TestClient,
    mock_jokes_db: Mock,
):
    joke_deleted = JokeModel(
        text=joke_model.text,
        number=joke_model.number,
        created_at=joke_model.created_at,
        updated_at=joke_model.updated_at,
        deleted_at=datetime.utcnow(),
    )

    mock_jokes_db.delete_joke = MagicMock()
    mock_jokes_db.delete_joke.return_value = joke_deleted

    resp = test_client.delete(f"/v1/jokes/{joke_model.number}")

    assert resp.json() == {
        "result": "deleted",
        "deleted": json.loads(joke_deleted.json(exclude_unset=True)),
    }
    assert resp.status_code == 200

    mock_jokes_db.delete_joke.assert_called_once_with(number=joke_model.number)
