import functools

import requests


def get_client_session() -> requests.Session:
    session = requests.Session()
    # Patch the request method to add timeouts. The tuple is (connect, read).
    session.request = functools.partial(session.request, timeout=(6.05, 27))  # type: ignore
    return session
