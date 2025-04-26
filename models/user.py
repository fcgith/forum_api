from datetime import datetime, date

from pydantic import BaseModel


class User(BaseModel):
    id: int | None
    username: str
    password: str
    email: str
    birthday: date
    avatar: str | None = None
    admin: int = 0
    creation_date: date

    @property
    def is_admin(self):
        return bool(self.admin)

class GetUsers(BaseModel):
    username: str
    token: str