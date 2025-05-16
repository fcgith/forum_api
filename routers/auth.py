from fastapi import Header

import mariadb
from fastapi import APIRouter
from models.auth_model import UserLogin, LoginResponse, RegisterResponse, UserCreate
from models.user import UserPublic
from services.auth import AuthService

router = APIRouter(tags=["auth"])


@router.post("/login", response_model=LoginResponse)
async def login(user_data: UserLogin) -> LoginResponse:
    """
    Authenticate a user with the provided credentials.

    Parameters
    ----------
    user_data : UserLogin
        The login data including username and password.

    Returns
    -------
    LoginResponse
        A response containing authentication tokens and user information.
    """
    return AuthService.login_user(user_data)


@router.post("/register", response_model=RegisterResponse)
async def register(user_data: UserCreate) -> RegisterResponse:
    """
    Register a new user with the provided information.

    Parameters
    ----------
    user_data : UserCreate
        The data required to create a new user account.

    Returns
    -------
    RegisterResponse
        A response indicating the result and status of the registration process.
    """
    return AuthService.register_user(user_data)


@router.get("/")
async def get_user_data_by_token\
                (token: Header(..., alias="Authorization")) -> UserPublic:
    """
    Retrieve public user information by decoding a JWT token.

    Parameters
    ----------
    token : str
        A JWT token used to identify and authenticate the user.

    Returns
    -------
    UserPublic or None
        The public user information if the token is valid, otherwise None.
    """
    return AuthService.decode_token_username(token)
