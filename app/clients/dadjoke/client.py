from typing import (
    Any,
    Dict,
)

from pydantic import (
    BaseModel,
)
from requests.exceptions import HTTPError
from typing import Literal

from app.clients import get_client_session
from app.clients.dadjoke.exceptions import (
    DadJokeClientError,
    DadJokeClientHttpError,
    DadJokeClientNotFoundError,
)
from app.logger import logger
from app.settings import API_DADJOKE_URL


def get_random_joke() -> str:
    return _request('GET', headers={"accept": "application/json"}, url="/")


def _request(
    method: Literal['GET', 'POST', 'PUT', 'DELETE', 'PATCH'],
    url: str,
    payload: BaseModel = None,
    headers: Dict[str, str] = None,
    params: Dict[str, Any] = None
) -> dict:
    headers = {**(headers if headers else {})}
    url = f'{API_DADJOKE_URL}' + (url if url.startswith('/') else f'/{url}')
    try:
        response = get_client_session().request(
            method,
            url,
            headers=headers,
            data=payload.json(exclude_unset=True) if payload else None,
            params=params,
        )
    except ConnectionError as ce:
        raise DadJokeClientError('Error in dadjoke client') from ce

    try:
        response.raise_for_status()
        logger.debug(f"Response from dadjoke, response={response.json()}")
        return response.json()
    except HTTPError as http_error:
        if response.status_code == 404:
            raise DadJokeClientNotFoundError(f'dadjoke client 404, response={response.text}') from http_error
        raise DadJokeClientHttpError(
            f'HTTP error in dadjoke client, status_code={response.status_code}, response={response.text}'
        ) from http_error
