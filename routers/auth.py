import mariadb
from fastapi import APIRouter, Depends, HTTPException, Form

from models.auth_model import UserLogin, LoginResponse, RegisterResponse, UserCreate
from services.errors import not_implemented
from services.utils import generate_token, decode_token

router = APIRouter(tags=["auth"])

@router.post("/login", response_model=LoginResponse)
async def login(user: UserLogin) -> LoginResponse:
    """
    Handles user login by validating the provided credentials and returning a
    login response containing authentication information. This endpoint is
    responsible for managing user authentication operations.
    """
    raise not_implemented

@router.post("/register", response_model=RegisterResponse)
async def register(user: UserCreate) -> RegisterResponse:
    """
    Registers a new user in the system.

    Handles the creation of a new user by taking user
    details provided and returning a response containing the registration status and other relevant information
    upon successful registration.
    """
    raise not_implemented