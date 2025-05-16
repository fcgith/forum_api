from typing import List

from models.message import Message, MessageCreate
from data.connection import read_query, insert_query


def gen_message(result: tuple) -> Message:
    return Message(
        id=result[0],
        content=result[1],
        date=result[2],
        conversation_id=result[3],
        sender_id=result[4]
    )


def get_messages_by_conversation(conversation_id: int) -> List[Message] | None:
    query = "SELECT * FROM messages WHERE conversation_id = ? ORDER BY date ASC"
    result = read_query(query, (conversation_id,))
    if result:
        messages = [gen_message(row) for row in result]
        return messages
    return None


def get_message_by_id(message_id: int) -> Message | None:
    query = "SELECT * FROM messages WHERE id = ?"
    result = read_query(query, (message_id,))
    if result:
        return gen_message(result[0])
    return None


def create_message(data: MessageCreate, conversation_id: int, sender_id: int) -> int | None:
    query = "INSERT INTO messages (content, conversation_id, sender_id, receiver_id) VALUES (?, ?, ?, ?)"
    result = insert_query(query, (data.content, conversation_id, sender_id, data.receiver_id))
    return result
