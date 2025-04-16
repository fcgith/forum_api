import mariadb
from fastapi import APIRouter, Depends, HTTPException, Form

from models.auth_model import UserLogin, LoginResponse, RegisterResponse, UserCreate
from services.errors import not_implemented
from services.utils import generate_token, decode_token

router = APIRouter(tags=["auth"])

@router.post("/login", response_model=LoginResponse)
async def login(user: UserLogin) -> LoginResponse:
    raise not_implemented

@router.post("/register", response_model=RegisterResponse)
async def register(user: UserCreate) -> RegisterResponse:
    raise not_implemented