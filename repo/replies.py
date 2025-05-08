from data.connection import read_query, update_query, insert_query
from models.reply import Reply

def gen_reply(reply: tuple) -> Reply:
    return Reply(id=reply[0],
                 content=reply[1],
                 date=reply[2],
                 topic_id=reply[3],
                 user_id=reply[4],
                 best_reply=reply[5])

def get_reply_by_id(reply_id: int) -> Reply | None:
    query = "SELECT * FROM replies WHERE id = ?"
    result = read_query(query, (reply_id,))
    return gen_reply(result[0]) if result else None

def set_reply_vote(reply_id: int, user_id: int, vote: int) -> bool | None:
    if vote not in (0, 1):
        vote = 0

    query = "SELECT * FROM votes WHERE reply_id = ? AND user_id = ?"
    result = read_query(query, (reply_id, user_id))
    if result:
        query = "UPDATE votes SET type = ? WHERE reply_id = ? AND user_id = ?"
        result = update_query(query, (vote, reply_id, user_id))
    else:
        query = "INSERT INTO votes (reply_id, user_id, type) VALUES (?, ?, ?)"
        result = insert_query(query, (reply_id, user_id, vote))

    return True if result else False

def get_reply_votes(reply_id: int) -> int:
    query = "SELECT type FROM votes WHERE reply_id = ?"
    result = read_query(query, (reply_id,))
    votes = [row[0] for row in result]
    end_result = 0
    for vote in votes:
        end_result += vote if vote == 1 else -1
    return end_result

def add_reply_to_topic(content: str, topic_id: int, user_id: int) -> int | None:
    query = "INSERT INTO replies (content, topic_id, user_id) VALUES (?, ?, ?)"
    result = insert_query(query, (content, topic_id, user_id))
    return result

def set_reply_as_best(reply_id: int, topic_id: int) -> bool | None:
    query = "SELECT * FROM replies WHERE topic_id = ? AND best_reply = 1"
    result = read_query(query, (topic_id,))
    if result:
        query = "UPDATE replies SET best_reply = 0 WHERE topic_id = ? AND best_reply = 1"
        result = update_query(query, (topic_id,))
        query = "UPDATE replies SET best_reply = 1 WHERE id = ?"
        result = update_query(query, (reply_id,))
        return True if result else False

    query = "UPDATE replies SET best_reply = 1 WHERE id = ?"
    result = update_query(query, (reply_id,))
    return True if result else False