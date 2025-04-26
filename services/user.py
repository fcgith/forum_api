from fastapi import HTTPException

from repo.user import get_user_by_id, get_user_by_username, get_all_users
from services.errors import access_denied, not_found
from services.utils import AuthToken


def get_user(user_id: int):
    user = get_user_by_id(user_id)
    if user:
        return user
    else:
        raise not_found

def get_users(username: str, token: str):
    user = get_user_by_username(username)
    if not user:
        print("not user")
        raise access_denied

    decoded_token = AuthToken.decode(token)
    if decoded_token.get("sub") != user.username or not user.is_admin():
        raise access_denied

    return get_all_users()
