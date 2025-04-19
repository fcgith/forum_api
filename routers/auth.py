import mariadb
from fastapi import APIRouter, Depends, HTTPException, Form

from models.auth_model import UserLogin, LoginResponse, RegisterResponse, UserCreate
from repo.connection import get_db
from services.errors import not_implemented, not_found, access_denied, internal_error
from services.utils import generate_token, decode_token
from repo import user as user

router = APIRouter(tags=["auth"])

@router.post("/login", response_model=LoginResponse)
async def login(user_data: UserLogin) -> LoginResponse:
    """
    Handles user login by validating the provided credentials and returning a
    login response containing authentication information. This endpoint is
    responsible for managing user authentication operations.
    """

    username = user_data.username
    user_db = user.get_user_by_username(username)
    if user_db:
        password = user_data.password
        if user_db[2] != password:
            raise access_denied
        token = generate_token({"username": username, })
        return LoginResponse(access_token=token, token_type="bearer")
    else:
        raise not_found

@router.post("/register", response_model=RegisterResponse)
async def register(user_data: UserCreate) -> RegisterResponse:
    """
    Registers a new user in the system.

    Handles the creation of a new user by taking user
    details provided and returning a response containing the registration status and other relevant information
    upon successful registration.
    """
    try:
        data = UserCreate(username=user_data.username,
                          password=user_data.password,
                          email=user_data.email,
                          birthday=user_data.birthday
)
        if not data:
            print(data)
            raise internal_error
        else:
            insert_query = """INSERT INTO users (username, password, email) VALUES (?, ?, ?)"""
            user_id = user.insert_query(insert_query, (data.username, data.password, data.email))

        return RegisterResponse(message=f"User {user_id} created successfully")

    except mariadb.Error as e:
        raise internal_error