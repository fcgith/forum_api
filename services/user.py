from typing import List

from models.user import User, UserPublic
from repo.user import get_user_by_id, get_user_by_username, get_all_users
from services.errors import access_denied, not_found
from services.utils import AuthToken

class UserService:

    @classmethod
    def get_user(cls, user_id: int, public: bool = False) -> User | UserPublic | None:
        user = get_user_by_id(user_id, public)
        if user:
            return user
        else:
            raise not_found

    @classmethod
    def get_users(cls, token: str, public: bool = False) -> List[User]:
        user = AuthToken.validate(token, public)

        if not user or not user.is_admin():
            raise access_denied

        return get_all_users()
