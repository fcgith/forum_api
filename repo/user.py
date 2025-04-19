from fastapi.params import Depends

from .connection import get_db, read_query, insert_query, update_query


def get_user_by_id(id: int):
    query = "SELECT * FROM users WHERE id = ?"
    result = read_query(query, (id,)).fetchone()
    return User(*result)
    # return {
    #     'id': id,
    #     'name': 'user' + str(id)
    # }

def get_user_by_username(username: str):
    query = "SELECT * FROM users WHERE username = ?"
    result = read_query(query, (username,)).fetchone()
    return result

