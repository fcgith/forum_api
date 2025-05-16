from typing import List
from fastapi import APIRouter, Header
from models.user import User, UserPublic
from services.user import UserService

router = APIRouter(tags=["user"])


@router.get("/", response_model=List[User])
async def get_all_users(token: str = Header(..., alias="Authorization")) -> List[User]:
    """
    Fetches and returns a list of all users if the authenticated user is valid and an admin.

    Parameters
    ----------
    token : str
        Header Authentication token used for user authentication and authorization.

    Returns
    -------
    List[User]
        A list of user objects.
    """
    return UserService.get_users(token)


@router.get("/me", response_model=UserPublic)
async def get_user_by_token \
                (token: str = Header(..., alias="Authorization")) -> UserPublic:
    """
    Retrieve public user information by decoding the authenticated user's JWT token.

    Parameters
    ----------
    token : str
        Header Authorization token

    Returns
    -------
    UserPublic
        The public user data if the token is valid.
    """
    return UserService.get_user_by_token(token, True)


@router.get("/{user_id}", response_model=UserPublic)
async def get_user_by_id(user_id: int) -> UserPublic:
    """
    Retrieve a user's public data by their ID number.

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


@router.get("/search/{username}", response_model=UserPublic)
def get_by_username(username: str,
                    token: str = Header(..., alias="Authorization")) -> UserPublic:
    """
    Gets public user data by username.

    Parameters
    ----------
    username : str
        Username to search for.
    token : str
        Header Authentication token.

    Returns
    -------
    UserPublic
        The user object containing detailed information about the user.
    """
    return UserService.get_user_by_username(username, token, True)


@router.put("/avatar/", response_model=dict)
async def update_avatar(link: str, token: str = Header(..., alias="Authorization")) -> dict:
    """
    Update user avatar.

    Parameters
    ----------
    token : str
        Head Authentication token.

    link : str
        Link to avatar image.

    Returns
    -------
        dict with a message notifying the success or failure of the operation.
    """
    return UserService.set_avatar(token, link)
