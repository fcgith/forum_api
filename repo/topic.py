from typing import List

from models.reply import Reply
from models.topic import Topic, TopicCreate
from data.connection import read_query, insert_query, update_query
from repo.replies import gen_reply
from repo.user import get_user_by_id
import repo.category as category_repo


def gen_topic(result: tuple) -> Topic:
    return Topic(
        id=result[0],
        name=result[1],
        content=result[2],
        date=result[3],
        category_id=result[4],
        category_name=category_repo.get_category_by_id(result[4]).name,
        user_id=result[5],
        user_name=get_user_by_id(result[5]).username if result[5] else None,
        replies_count=len(get_replies_by_topic_id(result[0])),
        locked=result[6])

def get_topic_by_id(topic_id: int) -> Topic | None:
    query = "SELECT * FROM topics WHERE id = ?"
    result = read_query(query, (topic_id,))
    if result:
        return gen_topic(result[0])
    return None

def get_topics_by_category(category_id: int) -> List[Topic] | None:
    query = "SELECT * FROM topics WHERE category_id = ? ORDER BY date DESC"
    result = read_query(query, (category_id,))
    if result:
        topics = [gen_topic(row) for row in result]
        return topics
    return None

def get_topics_count_by_category(category_id: int) -> int:
    query = "SELECT COUNT(*) FROM topics WHERE category_id = ?"
    result = read_query(query, (category_id,))
    if result:
        return result[0][0]
    return 0

def create_topic(data: TopicCreate, user_id: int) -> int | None:
    query = "INSERT INTO topics (name, content, category_id, user_id) VALUES (?, ?, ?, ?)"
    result = insert_query(query, (data.name, data.content, data.category_id, user_id))
    return result

def get_all_topics() -> dict:
    query = "SELECT * FROM topics"
    result = read_query(query)
    topics = [gen_topic(row) for row in result]
    pages = len(topics) // 10 + 1
    return {"pages": pages, "topics": topics}

def get_topics(search: str = None, sort: str = "DESC", page: int = 0, category_ids: list = None) -> dict | None:
    params = []
    if isinstance(sort, str):
        sort = sort.lower()
    else:
        sort = "desc"

    # Base query for counting total topics
    count_query = "SELECT COUNT(*) FROM topics"
    select_query = "SELECT * FROM topics"
    if category_ids and len(category_ids) > 0:
        placeholder = ", ".join(["?"] * len(category_ids))
        count_query += f" WHERE category_id IN ({placeholder})"
        select_query += f" WHERE category_id IN ({placeholder})"
        params.extend(category_ids)

    if search:
        search = search.replace("+", " ")
        if "WHERE" in count_query:
            count_query += " AND name LIKE ?"
            select_query += " AND name LIKE ?"
        else:
            count_query += " WHERE name LIKE ?"
            select_query += " WHERE name LIKE ?"
        params.append(f"%{search}%")

    # Execute count query to get total number of topics
    count_params = params.copy()
    total_topics = read_query(count_query, tuple(count_params))[0][0]

    # Add sorting to select query
    if sort == "asc":
        select_query += " ORDER BY id ASC"
    else:
        select_query += " ORDER BY id DESC"

    # Add pagination
    limit = 10
    offset = page * limit
    select_query += " LIMIT ? OFFSET ?"
    params.extend([limit, offset])

    result = read_query(select_query, tuple(params))
    topics = [gen_topic(row) for row in result] if result else []

    total_pages = total_topics // limit + 1

    return {"pages": total_pages, "topics": topics}


def get_replies_by_topic_id(topic_id: int) -> list[Reply]:
    """
    Get all replies for a specific topic.

    Args:
        topic_id: ID of the topic

    Returns:
        List of Reply objects
    """
    query = "SELECT * FROM replies WHERE topic_id = ? ORDER BY date ASC"
    results = read_query(query, (topic_id,))
    return [gen_reply(reply) for reply in results] if results else []


def get_topics_in_category(category_id) -> List[Topic] | []:
    query = "SELECT * FROM topics WHERE category_id = ? ORDER BY id DESC"
    result = read_query(query, (category_id,))
    return [gen_topic(row) for row in result] if result else []


def lock_topic(topic_id) -> bool:
    query = "UPDATE topics SET locked = 1 WHERE id = ?"
    result = update_query(query, (topic_id,))
    return True if result > 0 else False