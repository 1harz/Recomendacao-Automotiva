import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Query

from src.models import (
    HealthResponse,
    ItemCreate,
    RatingCreate,
    RecommendationItem,
    UserCreate,
)
from src.recommender import RecommenderSystem


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
REVIEWS_PATH = os.path.join(DATA_DIR, "amazon_reviews_automotive_sample.csv")
META_PATH = os.path.join(DATA_DIR, "amazon_meta_automotive_sample.csv")

recommender = RecommenderSystem()
users: dict[str, str] = {}
items: dict[str, str] = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    if recommender.total_reviews == 0:
        try:
            recommender.load_data(REVIEWS_PATH, META_PATH)
        except FileNotFoundError:
            pass
    yield


app = FastAPI(
    title="Automotive Recommendation API",
    description=(
        "API com Inteligencia Artificial de Recomendacao de pecas automotivas "
        "baseada em Filtragem Colaborativa (Similaridade de Cosseno) sobre o "
        "dataset Amazon Automotive 2023."
    ),
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/", tags=["Util"])
def read_root():
    return {
        "message": "Welcome to Automotive Recommendation API",
        "version": "1.0.0",
    }


@app.get("/health", response_model=HealthResponse, tags=["Util"])
def health_check():
    return recommender.stats()


@app.post("/users", tags=["Usuarios"])
def create_user(user: UserCreate):
    if user.user_id in users:
        raise HTTPException(status_code=400, detail="Usuario ja cadastrado")
    users[user.user_id] = user.name
    return {"user_id": user.user_id, "name": user.name}


@app.post("/items", tags=["Itens"])
def create_item(item: ItemCreate):
    if item.parent_asin in items:
        raise HTTPException(status_code=400, detail="Item ja cadastrado")
    items[item.parent_asin] = item.title
    return {"parent_asin": item.parent_asin, "title": item.title}


@app.get("/users", tags=["Usuarios"])
def get_users():
    return [{"user_id": uid, "name": name} for uid, name in users.items()]


@app.get("/items", tags=["Itens"])
def get_items():
    return [{"parent_asin": asin, "title": title} for asin, title in items.items()]


@app.post("/ratings", tags=["Avaliacoes"])
def add_rating(rating: RatingCreate):
    recommender.add_rating(rating.user_id, rating.parent_asin, rating.rating)
    return {
        "message": (
            f"Nota {rating.rating} do usuario {rating.user_id} "
            f"para o item {rating.parent_asin} registrada."
        )
    }


@app.get(
    "/recommendations/{user_id}",
    response_model=list[RecommendationItem],
    tags=["Recomendacoes"],
)
def get_recommendations(
    user_id: str,
    n: int = Query(5, ge=1, le=50, description="Quantidade de itens a recomendar"),
):
    return [RecommendationItem(**r) for r in recommender.recommend(user_id, n)]
