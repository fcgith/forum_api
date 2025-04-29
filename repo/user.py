from typing import List

from models.auth_model import UserCreate
from models.user import User, UserPublic
from data.connection import read_query, insert_query

def gen_user(result: tuple, public: bool = False) -> User | UserPublic:
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
    ) if not public else UserPublic(
        id=result[0],
        username=result[1],
        email=result[3],
        avatar=result[5],
        creation_date=result[7]
    )

def get_all_users() -> List[User] | None:
    """
    Returns all users if the requester is an admin and authenticated, non-public user data
    :return: User list
    """
    query = "SELECT * FROM users"
    result = read_query(query)
    users = [gen_user(row) for row in result]
    return users

def get_user_by_id(user_id: int, public: bool = False) -> User | None:
    """
    Returns User if such exists by id or UserPublic if such is requested via service
    :param user_id: int user id
    :param public: bool should private data be exposed
    :return: User or None
    """
    query = "SELECT * FROM users WHERE id = ?"
    result = read_query(query, (user_id,))
    if result:
        return gen_user(result[0], public)
    else:
        return None

def get_user_by_username(username: str, public: bool = False) -> User | None:
    """
    Returns User if such exists by username or UserPublic if such is requested via service
    :param username: str Username
    :param public: bool should private data be exposed
    :return: User or None
    """
    query = "SELECT * FROM users WHERE username = ?"
    result = read_query(query, (username,))
    if result:
        return gen_user(result[0], public)
    else:
        return None

def insert_user(data: UserCreate) -> int | None:
    """
    Adds a new user in the database
    :param data: User data to insert into the database
    :return: the ID of the created user
    """
    query = "INSERT INTO users (username, password, email, birthday) VALUES (?, ?, ?, ?)"
    result = insert_query(query,
                            (data.username,
                                    data.password,
                                    data.email,
                                    data.birthday))
    return result

def gen_users_in_list_by_id(lst: List[int], public: bool = False) -> List[User]:
    """
    Converts a list of IDs into a list of Users
    :param lst: List of user IDs
    :param public: bool should private data be exposed
    :return: List of User or UserPublic objects
    """
    return [get_user_by_id(user_id, public) for user_id in lst]