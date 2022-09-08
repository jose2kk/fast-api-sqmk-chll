import random
from typing import (
    List,
    Optional,
    Union,
)

from fastapi import (
    FastAPI,
    Query,
)

from app.database.operations import jokes as jokes_db
from app.schemas.jokes import (
    JokeCreateModel,
    JokesParamEnum,
    JokeUpdateModel,
)
from app.services.jokes import service as jokes_service
from app.services.mathematics import service as math_service

app = FastAPI()


@app.get("/v1/healthcheck")
def healthcheck_endpoint():
    return {"message": "up and running"}


@app.get("/v1/math")
def math_endpoint(numbers: Union[List[int], None] = Query(default=None), number: Union[int, None] = None):
    if number:
        return {"result": number + 1}
    elif numbers:
        return {"result": math_service.get_lcm(numbers)}


@app.get("/v1/jokes/")
@app.get("/v1/jokes/{param}")
def get_joke(param: Optional[JokesParamEnum] = Query(None)):
    if not param:
        joke = random.choice([
            jokes_service.get_dad_joke,
            jokes_service.get_chuck_norris_joke,
        ])()
        return {"result": joke}
    elif param == "dad":
        joke = jokes_service.get_dad_joke()
        return {"result": joke}
    elif param == "chuck":
        joke = jokes_service.get_chuck_norris_joke()
        return {"result": joke}


@app.post("/v1/jokes/", status_code=201)
def create_joke(joke: JokeCreateModel):
    joke_from_db = jokes_db.create_joke(joke=joke)
    return {
        "result": "joke created" if joke_from_db else "joke not created",
        "created": joke_from_db.dict(exclude_unset=True) if joke_from_db else None,
    }


@app.patch("/v1/jokes/{number}")
def update_joke(joke: JokeUpdateModel, number: int):
    joke_from_db = jokes_db.update_joke(number=number, joke=joke)
    return {
        "result": "updated" if joke_from_db else "could not update the resource",
        "updated": joke_from_db.dict(exclude_unset=True) if joke_from_db else None,
    }


@app.delete("/v1/jokes/{number}")
def delete_joke(number: int):
    joke_from_db = jokes_db.delete_joke(number=number)
    return {
        "result": "deleted" if joke_from_db else "it was not deleted",
        "deleted": joke_from_db.dict(exclude_unset=True) if joke_from_db else None,
    }
