from typing import List
from fastapi import APIRouter
from models.user import User, UserPublic
from services.user import UserService

router = APIRouter(tags=["user"])

@router.get("/", response_model=List[User])
async def get_all_users(token: str) -> List[User]:
    """
    Fetches and returns a list of all users with if the provided auth token is valid and the user is an admin.

    :param token: Token used for user authentication and authorization.
    :type token: str
    :return: A list of user objects.
    :rtype: List[User]
    """
    users = UserService.get_users(token)
    return users

@router.get("/{user_id}", response_model=User)
async def get_user_with_id(user_id: int) -> User | UserPublic:
    """
    Retrieve a user by their ID number.

    :param user_id: A unique identifier for the user to be retrieved.
    :type user_id: int
    :return: The user object containing detailed information about the user.
    :rtype: User
    """
    return UserService.get_user(user_id)