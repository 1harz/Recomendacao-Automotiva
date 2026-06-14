from fastapi.testclient import TestClient

import src.main as main


def test_app_metadata():
    assert main.app.title.startswith("Automotive")
    assert main.app.version == "1.0.0"


def test_core_routes_registered():
    paths = {route.path for route in main.app.routes}
    for expected in [
        "/",
        "/health",
        "/users",
        "/items",
        "/ratings",
        "/recommendations/{user_id}",
    ]:
        assert expected in paths


def test_root_endpoint():
    client = TestClient(main.app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["version"] == "1.0.0"
