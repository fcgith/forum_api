from typing import Optional
from pydantic import BaseModel
from models.category_permission import PermissionTypeEnum
from models.user import User


class Category(BaseModel):
    id: int
    name: str
    description: str | None = None
    hidden: int = 0
    locked: int = 0
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


class UpdateUserPermission(BaseModel):
    category_id: int
    user_id: int
    permission: int = 1

class PrivilegedUser(BaseModel):
    user: User
    permission: int