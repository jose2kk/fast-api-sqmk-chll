from fastapi.testclient import TestClient

from app.services.mathematics import service as math_service
from fixtures.client import test_client


def test_math_endpoint__number_query_param(
    test_client: TestClient,
):
    number = 5

    resp = test_client.get(f"/v1/math?number={number}")

    assert resp.json() == {"result": number + 1}
    assert resp.status_code == 200


def test_math_endpoint__numbers_query_param(
    test_client: TestClient,
):
    numbers = [2, 3, 4]

    resp = test_client.get(f"/v1/math?numbers={'&numbers='.join(map(str, numbers))}")

    assert resp.json() == {"result": math_service.get_lcm(numbers)}
    assert resp.status_code == 200
