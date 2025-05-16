from typing import List

from models.auth_model import UserCreate
from models.user import User, UserPublic
from data.connection import read_query, insert_query, update_query
from services.errors import not_found


def gen_user(result: tuple, public: bool = False) -> User | UserPublic:
    return User(
        id=result[0],
        username=result[1],
        password=result[2],
        email=result[3],
        birthday=result[4],
        avatar=result[5],
        admin=result[6],
        creation_date=result[7],
        special_permissions=get_user_category_permissions(result[0])
    ) if not public else UserPublic(
        id=result[0],
        username=result[1],
        avatar=result[5],
        creation_date=result[7],
        admin=result[6]
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


def get_user_by_id(user_id: int, public: bool = False, tup=False) -> User | tuple | None:
    """
    Returns User if such exists by id or UserPublic if such is requested via service
    :param user_id: int user id
    :param public: bool should private data be exposed
    :return: User, UserPublic or None
    """
    query = "SELECT * FROM users WHERE id = ?"
    result = read_query(query, (user_id,))
    if result:
        return gen_user(result[0], public) if not tup else result[0]
    else:
        return None


def get_user_by_username(username: str, public: bool = False) -> User | None:
    """
    Returns User if such exists by username or UserPublic if such is requested via service
    :param username: str Username
    :param public: bool should private data be exposed
    :return: User, UserPublic or None
    """
    query = "SELECT * FROM users WHERE username = ?"
    result = read_query(query, (username,))
    if result:
        return gen_user(result[0], public)
    else:
        return None


def get_user_by_email(email: str, public: bool = False) -> User | None:
    """
    Returns User if such exists by email or UserPublic if such is requested via service
    :param email: str Email
    :param public: bool should private data be exposed
    :return: User, UserPublic or None
    """
    query = "SELECT * FROM users WHERE email = ?"
    result = read_query(query, (email,))
    if result:
        return gen_user(result[0], public)
    else:
        return None


def user_exists(data: ()) -> bool:
    """
    Determines if a user exists in the database based on the provided
    username or email.

    :param data: tuple containing username and email
    :return: bool indicating if the user exists in the database
    """
    query = "SELECT * FROM users WHERE username = ? OR email = ?"
    result = read_query(query, data)
    return True if result else False


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


def get_users_in_list_by_id(lst: List[int], public: bool = False) -> List[User] | List[UserPublic]:
    """
    Converts a list of IDs into a list of User or UserPublic
    :param lst: List of user IDs
    :param public: bool should private data be exposed
    :return: List of User or UserPublic objects
    """
    return [get_user_by_id(user_id, public) for user_id in lst]


def get_users_with_permissions_for_category(category_id) -> list:
    query = "SELECT user_id, type FROM category_permissions WHERE category_id = ? AND type > 1"
    result = read_query(query, (category_id,))
    data = []
    if result:
        for row in result:
            data.append({"user": get_user_by_id(row[0]), "permission": row[1]})
    return data


def get_user_category_permissions(user_id: int) -> dict[int, int]:
    query = "SELECT category_id, type FROM category_permissions WHERE user_id = ?"
    result = read_query(query, (user_id,))
    data = {}
    if result:
        data = {row[0]: row[1] for row in result}
    return data


def get_last_message_between(user: User, user2: User) -> dict:
    query = "SELECT * FROM messages WHERE (sender_id = ? AND receiver_id = ?) OR (sender_id = ? AND receiver_id = ?) ORDER BY id DESC LIMIT 1"
    result = read_query(query, (user.id, user2.id, user2.id, user.id))
    data = {}
    if result:
        result = result[0]
        data = {
            "id": result[0],
            "content": result[1],
            "date": result[2],
            "conversation_id": result[3],
            "sender_id": result[4],
            "receiver_id": result[5]
        }
    return data


def get_users_in_conversation(conversation_id: int):
    query = "SELECT initiator_id, receiver_id FROM conversations WHERE id = ? LIMIT 1"
    result = read_query(query, (conversation_id,))
    if not result:
        raise not_found
    result = result[0]
    return get_users_in_list_by_id([result[0], result[1]])


def set_user_avatar(user: User, link: str):
    query = "UPDATE users SET avatar = ? WHERE id = ?"
    result = update_query(query, (link, user.id))
    return result
