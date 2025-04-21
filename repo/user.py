from models.auth_model import UserCreate
from models.user import User
from services.errors import not_found
from .connection import read_query, insert_query

def gen_user(result: tuple):
    # print(result)
    # raise Exception("test")
    return User(
        id=result[0],
        username=result[1],
        password=result[2],
        email=result[3],
        birthday=result[4],
        avatar=result[5],
        admin=result[6],
        creation_date=result[7]
    )

def get_user_by_id(user_id: int) -> User:
    try:
        query = "SELECT * FROM users WHERE id = ?"
        result = read_query(query, (user_id,)).fetchone()
        return gen_user(result)
    except Exception as e:
        print(e)
        raise e
        raise not_found

def get_user_by_username(username: str) -> User:
    try:
        query = "SELECT * FROM users WHERE username = ?"
        result = read_query(query, (username,)).fetchone()
        return gen_user(result)
    except Exception as e:
        raise not_found

def insert_user(data: UserCreate) -> int | None:
    try:
        query = "INSERT INTO users (username, password, email, birthday) VALUES (?, ?, ?, ?)"
        result = insert_query(query,
                                (data.username,
                                        data.password,
                                        data.email,
                                        data.birthday))
        return result
    except Exception as e:
        print(e)

