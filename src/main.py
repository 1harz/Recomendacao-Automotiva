from fastapi import FastAPI
from src.models import UserCreate

app = FastAPI(title='Automotive Recommendation API')


@app.get("/")
def read_root():
    return {"message": "Welcome to Automotive Recommendation API", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/users")
def create_user(user: UserCreate):
    return user
