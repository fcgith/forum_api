from pydantic import BaseModel

from ..repo.user import get_user_by_username


class User(BaseModel):
    id: int | None
    username: str
    password: str
    email: str
    birthday: int
    nickname: str | None = None
    admin: bool = False
    avatar: str | None = None
    creation_date: str | None = None

    def is_admin(self):
        return self.role == 'admin'

