from models.user import User
from .connection import read_query, insert_query


def get_user_by_id(id: int):
    query = "SELECT * FROM users WHERE id = ?"
    result = read_query(query, (id,)).fetchone()
    return result

def get_user_by_username(username: str):
    query = "SELECT * FROM users WHERE username = ?"
    result = read_query(query, (username,)).fetchone()
    return result

def insert_user(username: str, password: str, email: str, birth_date: str) -> int | None:
    try:
        query = "INSERT INTO users (username, password, email, birthdate) VALUES (?, ?, ?, ?)"
        result = insert_query(query, (username, password, email, birth_date))
        return result
    except Exception as e:
        print(e)
        return None

