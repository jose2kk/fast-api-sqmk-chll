from fastapi.testclient import TestClient

from fixtures.client import test_client


def test_healthcheck_endpoint(
    test_client: TestClient,
):
    resp = test_client.get("/v1/healthcheck")

    assert resp.json() == {"message": "up and running"}
    assert resp.status_code == 200
