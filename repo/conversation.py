from typing import List

from models.conversation import Conversation, ConversationCreate
from data.connection import read_query, insert_query

def conversation_exists(user_1_id: int, user_2_id: int) -> bool:
    query = "SELECT * FROM conversations WHERE initiator_id = ? AND receiver_id = ?"
    result = read_query(query, (user_1_id, user_2_id))
    if result:
        return True
    query = "SELECT * FROM conversations WHERE initiator_id = ? AND receiver_id = ?"
    result = read_query(query, (user_2_id, user_1_id))
    return True if result else False

def gen_conversation(result: tuple) -> Conversation:
    return Conversation(
        id=result[0],
        date=result[1],
        initiator_id=result[2],
        receiver_id=result[3],
        seen=result[4]
    )

def get_all_conversations() -> List[Conversation] | None:
    query = "SELECT * FROM conversations"
    result = read_query(query)
    if result:
        conversations = [gen_conversation(row) for row in result]
        return conversations
    return []

def get_conversation_by_id(conversation_id: int) -> Conversation | None:
    query = "SELECT * FROM conversations WHERE id = ?"
    result = read_query(query, (conversation_id,))
    if result:
        return gen_conversation(result[0])
    return None

def get_conversation_by_users(user_id: int, user_2_id: int) -> int | None:
    query = "SELECT * FROM conversations WHERE initiator_id = ? AND receiver_id = ?"
    result = read_query(query, (user_id, user_2_id))
    if result:
        return result[0][0]
    result=read_query(query, (user_2_id, user_id))
    if result:
        return result[0][0]
    return None
def get_conversations_by_user(user_id: int) -> List[Conversation] | None:
    query = "SELECT * FROM conversations WHERE initiator_id = ? OR receiver_id = ? ORDER BY id DESC"
    result = read_query(query, (user_id, user_id))
    return [gen_conversation(row) for row in result]


def get_conversation_between_users(user1_id: int, user2_id: int) -> Conversation | None:
    """
    Check if a conversation exists between two users (in either direction)

    Args:
        user1_id: ID of the first user
        user2_id: ID of the second user

    Returns:
        Conversation object if found, None otherwise
    """
    query = """
    SELECT * FROM conversations 
    WHERE (initiator_id = ? AND receiver_id = ?) 
    OR (initiator_id = ? AND receiver_id = ?)
    """
    result = read_query(query, (user1_id, user2_id, user2_id, user1_id))
    if result:
        return gen_conversation(result[0])
    return None

def create_conversation(initiator_id:int, receiver_id:int) -> int | None:

    query = "INSERT INTO conversations (initiator_id, receiver_id) VALUES (?, ?)"
    result = insert_query(query, (initiator_id, receiver_id))
    return result
