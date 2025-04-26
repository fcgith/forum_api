from typing import List

from fastapi import APIRouter

from models.user import User, GetUsers
from services.user import get_user, get_users

router = APIRouter(tags=["user"])

@router.get("/", response_model=List[User])
async def get_all_users(data: GetUsers):
    return get_users(data.username, data.token)

@router.get("/{user_id}", response_model=User)
async def get_user(user_id: int):
    return get_user(user_id)