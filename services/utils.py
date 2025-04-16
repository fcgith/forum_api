### File for stuff like JWT and etc.
from datetime import datetime, timedelta
import jwt
from jwt import encode, decode


ALGORITHM = "HS256" # JWT encoding algorithm
SECRET_KEY = "fh8q247ghf0qb8374fhq2847hf0q89734gfh7" # JWT encoding secret key


def generate_token(data: dict) -> str:
    """
    Generates an authentication token from provided data
    :param data: dict with data to encode
    :return: str with JWT token
    """

    # copy data to just in case
    encode_data = data.copy()

    # set expiry time for the authentication token
    encode_data['exp'] = datetime.now() + timedelta(minutes=60) # 1 hour

    #return encoded JWT token
    return jwt.encode(encode_data, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> dict:
    """
    Decodes an authentication token
    :param token: str with JWT token
    :return: dict with decoded data
    """

    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])