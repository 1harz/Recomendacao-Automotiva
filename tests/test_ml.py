import pandas as pd

from src.recommender import RecommenderSystem


def _build_rec() -> RecommenderSystem:
    ratings = pd.DataFrame(
        [
            {"user_id": "A", "parent_asin": "i1", "rating": 5},
            {"user_id": "A", "parent_asin": "i2", "rating": 4},
            {"user_id": "B", "parent_asin": "i1", "rating": 5},
            {"user_id": "B", "parent_asin": "i3", "rating": 4},
            {"user_id": "C", "parent_asin": "i2", "rating": 5},
            {"user_id": "C", "parent_asin": "i3", "rating": 3},
        ]
    )
    meta = pd.DataFrame(
        [
            {"parent_asin": "i1", "title": "Item 1", "average_rating": 4.8},
            {"parent_asin": "i2", "title": "Item 2", "average_rating": 4.5},
            {"parent_asin": "i3", "title": "Item 3", "average_rating": 3.7},
        ]
    )
    rec = RecommenderSystem()
    rec.load_from_dataframes(ratings, meta)
    return rec


def test_cold_start_returns_popular_for_unknown_user():
    rec = _build_rec()
    recs = rec.recommend("NOBODY", n=3)

    assert len(recs) > 0
    assert recs[0]["parent_asin"] == "i1"
    assert recs[0]["title"] == "Item 1"


def test_personalized_excludes_already_rated_items():
    rec = _build_rec()
    recs = rec.recommend("A", n=5)
    asins = [r["parent_asin"] for r in recs]

    assert "i1" not in asins
    assert "i2" not in asins
    assert "i3" in asins


def test_add_rating_updates_matrix():
    rec = _build_rec()
    before = rec.total_reviews

    rec.add_rating("D", "i1", 5)

    assert rec.total_reviews == before + 1
    assert "D" in rec.user_idx


def test_stats_reflect_loaded_data():
    rec = _build_rec()
    stats = rec.stats()

    assert stats["total_users"] == 3
    assert stats["total_items"] == 3
    assert stats["total_reviews"] == 6
    assert stats["status"] == "healthy"
