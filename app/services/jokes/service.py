from app.clients.chucknorris import client as chucknorris_client
from app.clients.dadjoke import client as dadjoke_client


def get_chuck_norris_joke() -> str:
    resp = chucknorris_client.get_random_joke()
    random_joke = resp.get("value")
    return random_joke


def get_dad_joke() -> str:
    resp = dadjoke_client.get_random_joke()
    random_joke = resp.get("joke")
    return random_joke
