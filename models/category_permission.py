from pydantic import BaseModel
from enum import Enum


class PermissionTypeEnum(Enum):
    NO_PERMISSION = 0
    NORMAL = 1
    SEE = 2
    WRITE_ACCESS = 3


class CategoryPermissionBase(BaseModel):
    category_id: int
    user_id: int
    type: PermissionTypeEnum


class CategoryPermissionCreate(CategoryPermissionBase):
    pass


class CategoryPermissionResponse(CategoryPermissionBase):
    id: int
