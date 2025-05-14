from datetime import datetime, date

from pydantic import BaseModel, field_validator


class User(BaseModel):
    id: int | None
    username: str
    password: str
    email: str
    birthday: date
    avatar: str | None = None
    admin: int = 0
    creation_date: date
    special_permissions: dict[int, int] = {}

    def is_admin(self):
        return self.admin > 0

class UserPublic(BaseModel):
    id: int | None
    username: str
    avatar: str | None = None
    creation_date: date
    admin: int = 0