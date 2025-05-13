from typing import List
from fastapi import APIRouter, Query, Body, Form, Path

from models.category import Category, CategoryCreate, UpdateHiddenStatus, UpdateUserPermission
from models.topic import Topic
from services.category import CategoryService
from services.user import UserService

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
async def get_category_by_id(category_id: int,token: str) -> Category:
    """
    Retrieve a category by its unique ID.

    :param category_id: The ID of the category.
    :param token: Authentication token for user validation.
    :return: Category object.
    """
    return CategoryService.get_by_id(category_id,token)

@router.get("/{category_id}/topics", response_model=List[Topic])
async def get_topics_by_category(category_id: int,token: str) -> List[Topic]:
    """
    Fetch and return a list of topics for a specified category.

    This function interacts with the `CategoryService` to retrieve a list
    of topics associated with the given category ID. The function expects
    the requester to provide a valid token for authorization.

    Args:
        category_id: An integer representing the unique ID of the category
            for which topics are to be fetched.
        token: A string containing the authorization token required to
            access this endpoint.

    Returns:
        A list of `Topic` objects representing the topics associated
        with the given category.

    Raises:
        HTTPException: If an error occurs during validation or if topics
            for the specified category cannot be retrieved.
    """
    return CategoryService.get_topics_by_category_id(category_id, token)

@router.post("/{category_id}", response_model=int)
async def create_category(data: CategoryCreate,token: str) -> int:
    """
    Create a new category with the given details.

    :param data: Category creation data.
    :param token: Authentication token for user validation.
    :return: ID of the created category.
    """
    return CategoryService.create(data,token)

@router.put("/update-hide-status", response_model=bool)
async def update_hide_status(token: str, data: UpdateHiddenStatus) -> bool:
    return CategoryService.update_hidden_status(data.category_id, data.hidden, token)


@router.put("/update-user-permissions", response_model=bool)
async def update_user_permissions(token: str, data: UpdateUserPermission) -> bool:
    return CategoryService.update_user_permissions(data.category_id, data.user_id, data.permission, token)

@router.get("{category_id}/get-users-with-permissions", response_model=dict)
async def get_users_with_view_or_read_perms(token: str, category_id: int) -> dict:
    return UserService.get_users_with_permissions_for_category(category_id, token)

@router.put("/{category_id}/hide")
async def hide_category(token: str, category_id: int) -> bool: # Obsolete
    return CategoryService.hide_category_by_id(category_id, token)