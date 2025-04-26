import mariadb
from fastapi import APIRouter
from models.auth_model import UserLogin, LoginResponse, RegisterResponse, UserCreate
import services.auth as auth_service

router = APIRouter(tags=["auth"])

@router.post("/login", response_model=LoginResponse)
async def login(user_data: UserLogin) -> LoginResponse:
    """
    Handles user login by validating the provided credentials and returning a
    login response containing authentication information. This endpoint is
    responsible for managing user authentication operations.
    """
    return auth_service.login_user(user_data)

@router.post("/register", response_model=RegisterResponse)
async def register(user_data: UserCreate) -> RegisterResponse:
    """
    Handles the creation of a new user by taking user
    details provided and returning a response containing the registration status and other relevant information
    upon successful registration.
    """
    print("here1")
    return auth_service.register_user(user_data)