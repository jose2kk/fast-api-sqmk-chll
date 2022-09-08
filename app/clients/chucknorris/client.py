from typing import (
    Any,
    Dict,
)

from pydantic import BaseModel
from requests.exceptions import HTTPError
from typing import Literal

from app.clients import get_client_session
from app.clients.chucknorris.exceptions import (
    ChuckNorrisClientError,
    ChuckNorrisClientHttpError,
    ChuckNorrisClientNotFoundError,
)
from app.logger import logger
from app.settings import API_CHUCKNORRIS_URL


def get_random_joke() -> str:
    return _request('GET', url="/jokes/random")


def _request(
    method: Literal['GET', 'POST', 'PUT', 'DELETE', 'PATCH'],
    url: str,
    payload: BaseModel = None,
    headers: Dict[str, str] = None,
    params: Dict[str, Any] = None
) -> dict:
    headers = {**(headers if headers else {})}
    url = f'{API_CHUCKNORRIS_URL}' + (url if url.startswith('/') else f'/{url}')
    try:
        response = get_client_session().request(
            method,
            url,
            headers=headers,
            data=payload.json(exclude_unset=True) if payload else None,
            params=params,
        )
    except ConnectionError as ce:
        raise ChuckNorrisClientError('Error in chucknorris client') from ce

    try:
        response.raise_for_status()
        logger.debug(f"Response from chucknorris, response={response.json()}")
        return response.json()
    except HTTPError as http_error:
        if response.status_code == 404:
            raise ChuckNorrisClientNotFoundError(f'chucknorris client 404, response={response.text}') from http_error
        raise ChuckNorrisClientHttpError(
            f'HTTP error in chucknorris client, status_code={response.status_code}, response={response.text}'
        ) from http_error
