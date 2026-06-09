from pydantic import BaseModel

class UserCreate(BaseModel):
    id: int
    name: str

class ItemCreate(BaseModel):
    id: int
    name: str

