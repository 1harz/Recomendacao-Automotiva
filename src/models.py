from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    user_id: str = Field(..., description="Identificador unico do usuario")
    name: str = Field(..., description="Nome do usuario")


class ItemCreate(BaseModel):
    parent_asin: str = Field(..., description="Identificador (ASIN) do produto automotivo")
    title: str = Field(..., description="Titulo do produto")


class RatingCreate(BaseModel):
    user_id: str = Field(..., description="Identificador do usuario que avaliou")
    parent_asin: str = Field(..., description="ASIN do item avaliado")
    rating: float = Field(
        ...,
        ge=1.0,
        le=5.0,
        description="Nota absoluta entre 1.0 e 5.0",
    )


class RecommendationItem(BaseModel):
    parent_asin: str
    title: str
    score: float


class RecommendationResponse(BaseModel):
    user_id: str
    recommendations: list[RecommendationItem]


class HealthResponse(BaseModel):
    status: str
    total_users: int
    total_items: int
    total_reviews: int
