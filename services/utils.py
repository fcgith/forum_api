### File for stuff like JWT and etc.
from datetime import datetime, timedelta
import jwt

from models.user import User, UserPublic
from repo.user import get_user_by_username
from services.errors import access_denied


class AuthToken:

    ALGORITHM = "HS256" # JWT encoding algorithm
    SECRET_KEY = "fh8q247ghf0qb8374fhq2847hf0q89734gfh7" # JWT encoding secret key

    @classmethod
    def generate(cls, data: dict) -> str:
        """
        Generates an authentication token from provided data
        :param data: dict with data to encode
        :return: str with JWT token
        """

        # copy data to just in case
        encode_data = data.copy()

        # set expiry time for the authentication token
        encode_data['exp'] = (datetime.now() + timedelta(minutes=60*8)).timestamp() # 8 hours

        #return encoded JWT token
        return jwt.encode(encode_data, cls.SECRET_KEY, algorithm=cls.ALGORITHM)

    @classmethod
    def decode(cls, token: str) -> dict:
        """
        Decodes an authentication token
        :param token: str with JWT token
        :return: dict with decoded data
        """

        return jwt.decode(token, cls.SECRET_KEY, algorithms=[cls.ALGORITHM])

    @classmethod
    def validate(cls, token: str, public: bool = False) -> User | UserPublic | bool:
        """
        Decodes and validates if an authentication token is valid
        :param token: str token
        :param public: bool if public data should be shared in response
        :return: bool is token valid or not
        """
        try:
            decoded = cls.decode(token)
            exp = decoded.get('exp')
            if exp:
                if datetime.now().timestamp() < exp:
                    user = get_user_by_username(decoded.get('sub'), public)
                    if not user:
                        raise access_denied
                    return user
            return False
        except jwt.ExpiredSignatureError:
            return False
        except jwt.InvalidTokenError:
            return False