from pydantic import BaseModel, validator, field_validator


class UserCreate(BaseModel):
    username: str
    password: str
    email: str
    birthday: str

class UserLogin(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str

class RegisterResponse(BaseModel):
    message: str