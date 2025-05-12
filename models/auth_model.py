from pydantic import BaseModel, validator, field_validator
import re

class UserCreate(BaseModel):
    username: str
    password: str
    email: str
    birthday: str

    @field_validator('username')
    def validate_username(cls, v):
        if len(v) < 6:
            raise ValueError('Username must be at least 6 characters long')
        elif len(v) > 16:
            raise ValueError('Username must be at most 16 characters long')
        elif not v.isalnum():
            raise ValueError('Username must be alphanumeric')
        elif v.replace("_", "").lower() in ['admin', 'root']:
            raise ValueError('Username cannot be "admin" or "root"')
        return v.lower()

    @field_validator('password')
    def validate_password(cls, v):
        if not len(v) >= 8:
            raise ValueError('Password must be at least 8 characters long')
        return v

    @field_validator('email')
    def validate_email(cls, v):
        if v.count('@') != 1:
            raise ValueError('Invalid email')
        return v

class UserLogin(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str

class RegisterResponse(BaseModel):
    message: str