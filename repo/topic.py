from typing import List

from models.topic import Topic, TopicCreate
from data.connection import read_query, insert_query

def gen_topic(result: tuple) -> Topic:
    return Topic(
        id=result[0],
        name=result[1],
        content=result[2],
        date=result[3],
        category_id=result[4],
        user_id=result[5]
    )

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

def create_topic(data: TopicCreate, user_id: int) -> int | None:
    query = "INSERT INTO topics (name, content, category_id, user_id) VALUES (?, ?, ?, ?)"
    result = insert_query(query, (data.name, data.content, data.category_id, user_id))
    return result

def get_topics(search: str = None, sort: str = "DESC", page: int = 0, category_ids: list = None) -> List[Topic]:
    params=[]
    sort = sort.lower()

    if category_ids and len(category_ids) > 0:
        placeholder = ", ".join(["?"] * len(category_ids))
        query = f"SELECT * FROM topics WHERE category_id IN ({placeholder})"
        params.extend(category_ids)
    else:
        query = "SELECT * FROM topics"

    if search:
        search = search.replace("+", " ")
        if "WHERE" in query:
            query += " AND name LIKE ?"
        else:
            query += " WHERE name LIKE ?"
        params.append(f"%{search}%")

    if sort == "asc":
        query += " ORDER BY id ASC"
    else:
        query += " ORDER BY id DESC"

    limit = 10
    offset = page * limit
    query += " LIMIT ? OFFSET ?"
    params.extend([limit, offset])

    result = read_query(query, tuple(params))
    if result:
        return [gen_topic(row) for row in result]
    return []