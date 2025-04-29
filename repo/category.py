from typing import List
from models.category import Category, CategoryCreate
from data.connection import read_query, insert_query

def gen_category(result: tuple) -> Category:
    return Category(
        id=result[0],
        name=result[1],
        description=result[2]
    )

def get_all_categories() -> List[Category] | None:
    query = "SELECT * FROM categories"
    result = read_query(query)
    if result:
        return [gen_category(row) for row in result]
    return []

def get_category_by_id(category_id: int) -> Category | None:
    query = "SELECT * FROM categories WHERE id = ?"
    result = read_query(query, (category_id,))
    if result:
        return gen_category(result[0])
    return None

def create_category(data: CategoryCreate) -> int | None:
    query = "INSERT INTO categories (name, description) VALUES (?, ?)"
    return insert_query(query, (data.name, data.description))
