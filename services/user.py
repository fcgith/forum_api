from repo.user import get_user_by_id, get_user_by_username, get_all_users
from services.errors import access_denied, not_found
from services.utils import AuthToken

class UserService:

    @classmethod
    def get_user(cls, user_id: int):
        user = get_user_by_id(user_id)
        if user:
            return user
        else:
            raise not_found

    @classmethod
    def get_users(cls, token: str):
        user = AuthToken.validate(token)

        if not user or not user.is_admin():
            raise access_denied

        return get_all_users()
