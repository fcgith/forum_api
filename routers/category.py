from typing import List
from fastapi import APIRouter

from models.category import Category, CategoryCreate
from services.category import CategoryService

router = APIRouter(tags=["categories"])


@router.get("/", response_model=List[Category])
async def get_all_categories(token: str) -> List[Category]:
    """
    Retrieve a list of all available categories.

    :param token: Authentication token.
    :return: List of Category objects.
    """
    return CategoryService.get_all_viewable(token)


@router.get("/{category_id}", response_model=Category)
async def get_category_by_id(category_id: int) -> Category:
    """
    Retrieve a category by its unique ID.

    :param category_id: The ID of the category.
    :return: Category object.
    """
    return CategoryService.get_by_id(category_id)


@router.post("/", response_model=int)
async def create_category(data: CategoryCreate) -> int:
    """
    Create a new category with the given details.

    :param data: Category creation data.
    :return: ID of the created category.
    """
    return CategoryService.create(data)