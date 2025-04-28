from typing import List
from fastapi import APIRouter
from models.user import User, GetUsers
from services.user import UserService

router = APIRouter(tags=["user"])

@router.post("/", response_model=List[User])
async def get_all_users(data: GetUsers):
    users = UserService.get_users(data.username, data.token)
    return users

@router.get("/{user_id}", response_model=User)
async def get_user_with_id(user_id: int):
    return UserService.get_user(user_id)