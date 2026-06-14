import pandas as pd
import pytest
from fastapi.testclient import TestClient

import src.main as main
from src.recommender import RecommenderSystem


def _sample_ratings():
    return pd.DataFrame(
        [
            {"user_id": "A", "parent_asin": "i1", "rating": 5},
            {"user_id": "A", "parent_asin": "i2", "rating": 4},
            {"user_id": "B", "parent_asin": "i1", "rating": 5},
            {"user_id": "B", "parent_asin": "i3", "rating": 4},
            {"user_id": "C", "parent_asin": "i2", "rating": 5},
            {"user_id": "C", "parent_asin": "i3", "rating": 3},
        ]
    )


def _sample_meta():
    return pd.DataFrame(
        [
            {"parent_asin": "i1", "title": "Item 1", "average_rating": 4.8},
            {"parent_asin": "i2", "title": "Item 2", "average_rating": 4.5},
            {"parent_asin": "i3", "title": "Item 3", "average_rating": 3.7},
        ]
    )


@pytest.fixture()
def client():
    rec = RecommenderSystem()
    rec.load_from_dataframes(_sample_ratings(), _sample_meta())
    main.recommender = rec
    main.users.clear()
    main.items.clear()
    with TestClient(main.app) as c:
        yield c
    main.recommender = RecommenderSystem()


def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "healthy"
    assert body["total_users"] == 3
    assert body["total_reviews"] == 6


def test_create_user_and_duplicate(client):
    response = client.post("/users", json={"user_id": "U1", "name": "Teste"})
    assert response.status_code == 200

    duplicate = client.post("/users", json={"user_id": "U1", "name": "Teste"})
    assert duplicate.status_code == 400


def test_create_item(client):
    response = client.post("/items", json={"parent_asin": "iX", "title": "Peca"})
    assert response.status_code == 200
    assert response.json()["parent_asin"] == "iX"


def test_rating_out_of_range_rejected(client):
    too_high = client.post(
        "/ratings", json={"user_id": "A", "parent_asin": "i1", "rating": 6.0}
    )
    assert too_high.status_code == 422

    too_low = client.post(
        "/ratings", json={"user_id": "A", "parent_asin": "i1", "rating": 0.5}
    )
    assert too_low.status_code == 422


def test_rating_valid_accepted(client):
    response = client.post(
        "/ratings", json={"user_id": "A", "parent_asin": "i3", "rating": 5.0}
    )
    assert response.status_code == 200
    assert "registrada" in response.json()["message"]


def test_recommendations_cold_start(client):
    response = client.get("/recommendations/NOBODY?n=3")
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)
    assert len(body) > 0
    assert body[0]["parent_asin"] == "i1"


def test_recommendations_personalized_excludes_rated(client):
    response = client.get("/recommendations/A?n=5")
    assert response.status_code == 200
    asins = [r["parent_asin"] for r in response.json()]
    assert "i1" not in asins
    assert "i2" not in asins
    assert "i3" in asins
