from typing import List

from models.category import PrivilegedUser
from models.user import User, UserPublic
import repo.user as user_repo
from services.errors import access_denied, not_found, internal_error, user_not_found, invalid_token
from services.utils import AuthToken


class UserService:

    @classmethod
    def get_user(cls, user_id: int, public: bool = False) -> User | UserPublic | None:
        user = user_repo.get_user_by_id(user_id, public)
        if user:
            return user
        else:
            raise user_not_found

    @classmethod
    def get_users(cls, token: str, public: bool = False) -> List[User]:
        AuthToken.validate_admin(token, public)

        return user_repo.get_all_users()

    @classmethod
    def get_users_with_permissions_for_category(cls, category_id: int, token: str) -> list[PrivilegedUser]:
        AuthToken.validate_admin(token)
        return user_repo.get_users_with_permissions_for_category(category_id)

    @classmethod
    def get_user_by_username(cls, username: str, token: str, public: bool = False):
        AuthToken.validate(token)
        user = user_repo.get_user_by_username(username, public)
        if user:
            return user
        else:
            raise user_not_found

    @classmethod
    def set_avatar(cls, token, link) -> dict:
        user = AuthToken.validate(token)
        user_repo.set_user_avatar(user, link)
        return {"message": "Avatar set successfully"}

    @classmethod
    def get_user_by_token(cls, token, public: bool = True):
        if AuthToken.validate_expiry(token):
            user = AuthToken.validate(token, public=public)
            if not user:
                raise invalid_token
            return user
        raise invalid_token
