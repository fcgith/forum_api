from typing import Optional
from pydantic import BaseModel
from models.category_permission import PermissionTypeEnum

class Category(BaseModel):
    id: int
    name: str
    description: str | None = None
    hidden: int = 0
    topics_count: int = 0


class CategoryCreate(BaseModel):
    name: str
    description: str | None = None


class CategoryResponse(Category):
    content: str
    user_permission: Optional[PermissionTypeEnum] = None

class UpdateHiddenStatus(BaseModel):
    category_id: int
    hidden: int = 0
