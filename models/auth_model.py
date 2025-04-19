from datetime import datetime

from pydantic import BaseModel
from typing import Union, Literal

class UserCreate(BaseModel):
    username: str
    password: str
    email: str
    birthday: int
    nickname: str | None = None

class UserLogin(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str

class RegisterResponse(BaseModel):
    message: str