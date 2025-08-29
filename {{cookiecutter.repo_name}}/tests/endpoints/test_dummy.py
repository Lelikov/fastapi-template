from collections.abc import Callable

from {{cookiecutter.project_name}}.endpoints.dummy import DummyEndpoint


async def test_dummy(test_client: Callable) -> None:
    endpoint: DummyEndpoint = DummyEndpoint()

    with test_client([endpoint.router]) as client:
        resp = await client.get("/dummy")

    assert resp.status_code == 200
    assert resp.json() is None

    with test_client([endpoint.router]) as client:
        resp = await client.get("/dummy-not-found")

    assert resp.status_code == 404
    assert resp.json() == {"detail": "Not Found"}
