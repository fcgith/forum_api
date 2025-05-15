from typing import List

from models.user import User, UserPublic
import repo.user as user_repo
from services.errors import access_denied, not_found, internal_error
from services.utils import AuthToken

class UserService:

    @classmethod
    def get_user(cls, user_id: int, public: bool = False) -> User | UserPublic | None:
        user = user_repo.get_user_by_id(user_id, public)
        if user:
            return user
        else:
            raise not_found

    @classmethod
    def get_users(cls, token: str, public: bool = False) -> List[User]:
        AuthToken.validate_admin(token, public)

        return user_repo.get_all_users()

    @classmethod
    def get_users_with_permissions_for_category(cls, category_id: int, token: str) -> dict:
        AuthToken.validate_admin(token)
        return user_repo.get_users_with_permissions_for_category(category_id)

    @classmethod
    def get_user_by_username(cls, username: str, public: bool = False):
        user = user_repo.get_user_by_username(username, public)
        if user:
            return user
        else:
            raise not_found

    @classmethod
    def set_avatar(cls, token, link):
         user = AuthToken.validate(token)
         result = user_repo.set_user_avatar(user, link)
         return result