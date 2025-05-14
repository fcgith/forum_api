from typing import List
from fastapi import APIRouter
from models.user import User, UserPublic
from services.user import UserService

router = APIRouter(tags=["user"])

@router.get("/", response_model=List[User])
async def get_all_users(token: str) -> List[User]:
    """
    Fetches and returns a list of all users if the provided auth token is valid and the user is an admin.

    Parameters
    ----------
    token : str
        Token used for user authentication and authorization.

    Returns
    -------
    List[User]
        A list of user objects.
    """
    users = UserService.get_users(token)
    return users

@router.get("/{user_id}")
async def get_user_with_id(user_id: int) -> User | UserPublic:
    """
    Retrieve a user by their ID number.

    Parameters
    ----------
    user_id : int
        A unique identifier for the user to be retrieved.

    Returns
    -------
    User | UserPublic
        The user object containing detailed information about the user.
    """
    return UserService.get_user(user_id, True)

@router.get("/get-by-username/{username}")
def get_by_username(username: str):
    return UserService.get_user_by_username(username, True)