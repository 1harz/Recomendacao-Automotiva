import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.metrics.pairwise import cosine_similarity


class RecommenderSystem:
    """Motor de recomendacao baseado em filtragem colaborativa por usuario.

    Constroi uma matriz esparsa usuario-item a partir das avaliacoes e utiliza
    Similaridade de Cosseno para encontrar usuarios parecidos. Para usuarios sem
    historico (Cold Start) retorna os itens mais populares do catalogo.
    """

    def __init__(self):
        self.ratings = pd.DataFrame(columns=["user_id", "parent_asin", "rating"])
        self.meta = pd.DataFrame(columns=["parent_asin", "title", "average_rating"])
        self.user_ids: list[str] = []
        self.item_ids: list[str] = []
        self.user_idx: dict[str, int] = {}
        self.item_idx: dict[str, int] = {}
        self.matrix = None
        self.presence = None
        self._title_map: dict[str, str] = {}
        self._avg_map: dict[str, float] = {}
        self._item_counts: dict[str, int] = {}
        self._popular: list[dict] = []

    # ------------------------------------------------------------------ carga
    def load_data(self, reviews_path: str, meta_path: str):
        ratings = pd.read_csv(reviews_path)
        ratings = ratings[["user_id", "parent_asin", "rating"]]
        meta = pd.read_csv(meta_path)
        meta = meta[["parent_asin", "title", "average_rating"]]
        self.load_from_dataframes(ratings, meta)

    def load_from_dataframes(self, ratings_df: pd.DataFrame, meta_df: pd.DataFrame):
        self.ratings = ratings_df[["user_id", "parent_asin", "rating"]].copy()
        self.ratings["rating"] = pd.to_numeric(self.ratings["rating"], errors="coerce")
        self.ratings = self.ratings.dropna(subset=["rating"])

        self.meta = meta_df[["parent_asin", "title", "average_rating"]].copy()
        self.meta["average_rating"] = (
            pd.to_numeric(self.meta["average_rating"], errors="coerce").fillna(0.0)
        )
        self._build()

    # -------------------------------------------------------------- construcao
    def _build(self):
        self.ratings = self.ratings.dropna(subset=["user_id", "parent_asin"])

        self.user_ids = sorted(self.ratings["user_id"].astype(str).unique())
        self.item_ids = sorted(self.ratings["parent_asin"].astype(str).unique())
        self.user_idx = {u: i for i, u in enumerate(self.user_ids)}
        self.item_idx = {it: j for j, it in enumerate(self.item_ids)}

        self._title_map = dict(zip(self.meta["parent_asin"], self.meta["title"]))
        self._avg_map = dict(
            zip(self.meta["parent_asin"], self.meta["average_rating"])
        )
        self._item_counts = (
            self.ratings.groupby("parent_asin").size().to_dict()
        )

        n_users, n_items = len(self.user_ids), len(self.item_ids)
        if n_users and n_items:
            rows = (
                self.ratings["user_id"].astype(str).map(self.user_idx).to_numpy()
            )
            cols = (
                self.ratings["parent_asin"]
                .astype(str)
                .map(self.item_idx)
                .to_numpy()
            )
            vals = self.ratings["rating"].to_numpy(dtype=float)
            self.matrix = csr_matrix(
                (vals, (rows, cols)), shape=(n_users, n_items)
            )
            self.presence = self.matrix.copy()
            self.presence.data = np.ones_like(self.presence.data)
        else:
            self.matrix = None
            self.presence = None

        self._popular = self._compute_popular()

    def _compute_popular(self) -> list[dict]:
        if self.meta.empty:
            return []
        df = self.meta.copy()
        df["count"] = df["parent_asin"].map(self._item_counts).fillna(0)
        df = df.sort_values(
            ["average_rating", "count"], ascending=[False, False]
        )
        return [
            {
                "parent_asin": str(row.parent_asin),
                "title": str(row.title),
                "score": round(float(row.average_rating), 2),
            }
            for row in df.itertuples()
        ]

    # ------------------------------------------------------------- metadados
    @property
    def total_users(self) -> int:
        return len(self.user_ids)

    @property
    def total_items(self) -> int:
        return len(self.meta)

    @property
    def total_reviews(self) -> int:
        return len(self.ratings)

    def stats(self) -> dict:
        return {
            "status": "healthy",
            "total_users": self.total_users,
            "total_items": self.total_items,
            "total_reviews": self.total_reviews,
        }

    # --------------------------------------------------------- recomendacao
    def get_popular_items(self, n: int = 5) -> list[dict]:
        return self._popular[:n]

    def recommend(self, user_id: str, n: int = 5) -> list[dict]:
        if self.matrix is None or str(user_id) not in self.user_idx:
            return self.get_popular_items(n)

        u = self.user_idx[str(user_id)]
        user_vec = self.matrix.getrow(u)

        sims = cosine_similarity(user_vec, self.matrix)[0]
        sims[u] = 0.0
        positive = np.clip(sims, 0.0, None)
        if positive.max() <= 0:
            return self.get_popular_items(n)

        numer = self.matrix.T.dot(positive)
        denom = self.presence.T.dot(positive)
        with np.errstate(divide="ignore", invalid="ignore"):
            scores = np.asarray(numer / denom).ravel()
        scores = np.nan_to_num(scores, nan=0.0, posinf=0.0, neginf=0.0)

        rated = user_vec.nonzero()[1]
        scores[rated] = -np.inf

        results = []
        for idx in np.argsort(scores)[::-1]:
            if len(results) >= n:
                break
            if scores[idx] <= 0:
                continue
            asin = self.item_ids[idx]
            results.append(
                {
                    "parent_asin": asin,
                    "title": self._title_map.get(asin, ""),
                    "score": round(float(scores[idx]), 2),
                }
            )
        return results or self.get_popular_items(n)

    # ----------------------------------------------------------- atualizacao
    def add_rating(self, user_id: str, parent_asin: str, rating: float):
        self.ratings.loc[len(self.ratings)] = [str(user_id), str(parent_asin), float(rating)]
        if str(parent_asin) not in self._title_map:
            self.meta.loc[len(self.meta)] = [str(parent_asin), "", float(rating)]
        self._build()
