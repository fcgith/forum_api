
from pydantic import BaseModel


class Category(BaseModel):
    id: int
    name: str
    description: str | None = None


class CategoryCreate(BaseModel):
    name: str
    description: str | None = None


class CategoryResponse(Category):
    content: str
