from typing import List

from models.conversation import Conversation, ConversationCreate
from data.connection import read_query, insert_query

def gen_conversation(result: tuple) -> Conversation:
    return Conversation(
        id=result[0],
        date=result[1],
        initiator_id=result[2],
        receiver_id=result[3]
    )

def get_all_conversations() -> List[Conversation] | None:
    query = "SELECT * FROM conversations"
    result = read_query(query)
    if result:
        conversations = [gen_conversation(row) for row in result]
        return conversations
    return None

def get_conversation_by_id(conversation_id: int) -> Conversation | None:
    query = "SELECT * FROM conversations WHERE id = ?"
    result = read_query(query, (conversation_id,))
    if result:
        return gen_conversation(result[0])
    return None

def get_conversations_by_user(user_id: int) -> List[Conversation] | None:
    query = "SELECT * FROM conversations WHERE initiator_id = ? OR receiver_id = ?"
    result = read_query(query, (user_id, user_id))
    if result:
        conversations = [gen_conversation(row) for row in result]
        return conversations
    return None

def create_conversation(data: ConversationCreate) -> int | None:
    query = "INSERT INTO conversations (initiator_id, receiver_id) VALUES (?, ?)"
    result = insert_query(query, (data.initiator_id, data.receiver_id))
    return result