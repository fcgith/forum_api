from datetime import datetime, timedelta, timezone
import jwt
from typing import Dict

from models.user import User, UserPublic
from repo.user import get_user_by_username
from services.errors import access_denied, invalid_token, internal_error


class AuthToken:
    ALGORITHM = "HS256"
    SECRET_KEY = "fh8q247ghf0qb8374fhq2847hf0q89734gfh7"

    @classmethod
    def generate(cls, data: dict) -> str:
        ## TODO: docstring
        encode_data = data.copy()
        encode_data['exp'] = (datetime.now(timezone.utc) + timedelta(minutes=60 * 8)).timestamp()
        token = jwt.encode(encode_data, cls.SECRET_KEY, algorithm=cls.ALGORITHM)
        # Ensure the token is a string
        if isinstance(token, bytes):
            token = token.decode('utf-8')
        return token

    @classmethod
    def decode(cls, token: str) -> Dict:
        ## TODO: docstring
        if isinstance(token, bytes):
            token = token.decode('utf-8')
        elif not isinstance(token, str):
            raise invalid_token
        try:
            decoded = jwt.decode(token, cls.SECRET_KEY, algorithms=[cls.ALGORITHM])
            return decoded
        except jwt.InvalidTokenError as e:
            print(f"Decode error: {str(e)}")
            raise invalid_token

    @classmethod
    def validate_expiry(cls, token: str) -> bool:
        try:
            decoded = cls.decode(token)
            exp = decoded.get('exp')
            if exp is None or not isinstance(exp, (int, float)):
                raise invalid_token
            current_time = datetime.now(timezone.utc).timestamp()
            return current_time < exp
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError) as e:
            print(f"Token validation error: {str(e)}")
            raise invalid_token

    @classmethod
    def validate(cls, token: str, public: bool = False) -> User | UserPublic | bool:
        """
        Returns user data if the token is valid or raises an error.
        """
        valid_date = cls.validate_expiry(token)
        if valid_date:
            try:
                username = cls.decode(token).get("sub")
                user = get_user_by_username(username, public)
                if not user:
                    raise access_denied
                return user
            except (jwt.ExpiredSignatureError, jwt.InvalidTokenError) as e:
                print(f"Token validation error: {e}")
                raise invalid_token
        raise access_denied

    @classmethod
    def validate_admin(cls, token: str, public: bool = False) -> None | User:
        ## TODO: docstring
        user = cls.validate(token, public=public)
        if user.is_admin():
            return user
        raise access_denied
