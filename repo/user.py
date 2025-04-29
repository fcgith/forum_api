from typing import List

from models.auth_model import UserCreate
from models.user import User
from data.connection import read_query, insert_query

def gen_user(result: tuple) -> User:
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

def get_all_users() -> List[User] | None:
    query = "SELECT * FROM users"
    result = read_query(query)
    users = [gen_user(row) for row in result]
    return users

def get_user_by_id(user_id: int) -> User | None:
    query = "SELECT * FROM users WHERE id = ?"
    result = read_query(query, (user_id,))
    if result:
        return gen_user(result[0])
    else:
        return None

def get_user_by_username(username: str) -> User | None:
    query = "SELECT * FROM users WHERE username = ?"
    result = read_query(query, (username,))
    if result:
        return gen_user(result[0])
    else:
        return None

def insert_user(data: UserCreate) -> int | None:
    query = "INSERT INTO users (username, password, email, birthday) VALUES (?, ?, ?, ?)"
    result = insert_query(query,
                            (data.username,
                                    data.password,
                                    data.email,
                                    data.birthday))
    return result

def gen_users_in_list_by_id(lst: List[int]) -> List[User]:
    return [get_user_by_id(user_id) for user_id in lst]