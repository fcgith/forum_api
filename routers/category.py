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

    Parameters
    ----------
    token : str
        Authentication token.

    Returns
    -------
    List[Category]
        A list of available categories the user can view.
    """
    return CategoryService.get_all_viewable(token)


@router.get("/{category_id}", response_model=Category)
async def get_category_by_id(category_id: int,token: str) -> Category:
    """
    Retrieve a category by its unique ID.

    Parameters
    ----------
    category_id : int
        The ID of the category.
    token : str
        Authentication token for user validation.

    Returns
    -------
    Category
        The category with the given ID.
    """
    return CategoryService.get_by_id(category_id,token)

@router.get("/{category_id}/topics", response_model=List[Topic])
async def get_topics_by_category(category_id: int,token: str) -> List[Topic]:
    """
    Retrieve a list of topics associated with a specific category.

    Parameters
    ----------
    category_id : int
        The ID of the category.
    token : str
        Authentication token for user authorization.

    Returns
    -------
    List[Topic]
        A list of topics under the specified category.
    """
    return CategoryService.get_topics_by_category_id(category_id, token)

@router.post("/add", response_model=int)
async def create_category(data: CategoryCreate,token: str) -> int:
    """
    Create a new category with the given details.

    Parameters
    ----------
    data : CategoryCreate
        The data required to create a new category.
    token : str
        Authentication token for user validation.

    Returns
    -------
    int
        The ID of the newly created category.
    """
    return CategoryService.create(data,token)

@router.put("/update-hide-status", response_model=bool)
async def update_hide_status(token: str, data: UpdateHiddenStatus) -> bool:
    """
    Update the visibility (hidden status) of a category.

    Parameters
    ----------
    token : str
        Authentication token.
    data : UpdateHiddenStatus
        Data containing the category ID and new hidden status.

    Returns
    -------
    bool
        True if the update was successful, False otherwise.
    """
    return CategoryService.update_hidden_status(data.category_id, data.hidden, token)


@router.put("/update-user-permissions", response_model=bool)
async def update_user_permissions(token: str, data: UpdateUserPermission) -> bool:
    """
    Update a user's permission level for a specific category.

    Parameters
    ----------
    token : str
        Authentication token.
    data : UpdateUserPermission
        Data containing category ID, user ID, and permission level.

    Returns
    -------
    bool
        True if the update was successful, False otherwise.
    """
    return CategoryService.update_user_permissions(data.category_id, data.user_id, data.permission, token)

@router.get("/{category_id}/get-users-with-permissions", response_model=list)
async def get_users_with_view_or_read_perms(token: str, category_id: int) -> list:
    """
    Retrieve users who have view or read permissions for a given category.

    Parameters
    ----------
    token : str
        Authentication token.
    category_id : int
        The ID of the category.

    Returns
    -------
    dict
        A dictionary mapping user IDs to their permission levels.
    """
    return UserService.get_users_with_permissions_for_category(category_id, token)

@router.get("/{category_id}/check-permission")
async def check_authenticated_user_category_permission(token: str, category_id: int):
    """
    Check the permission level (read/write) of the authenticated user for a category.

    Parameters
    ----------
    token : str
        Authentication token.
    category_id : int
        The ID of the category.

    Returns
    -------
    dict
        A dictionary with the key 'access_type' indicating permission level.
    """
    return {"access_type": CategoryService.get_read_or_write_permission(category_id, token)}

@router.put("/{category_id}/lock")
async def lock_category(token: str, category_id: int):
    return CategoryService.category_lock(category_id, token)
