from typing import List, Tuple
from models.category import Category, CategoryCreate
from models.category_permission import PermissionTypeEnum
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

def get_categories_with_permissions(user_id: int) -> List[Tuple[Category, PermissionTypeEnum]]:
    query = "SELECT c.id, c.name, c.description, cp.type FROM categories c LEFT JOIN category_permissions cp ON c.id = cp.category_id AND cp.user_id = ?"
    result = read_query(query, (user_id,))
    categories = []
    for row in result:
        category = Category(id=row[0], name=row[1], description=row[2])
        permission = PermissionTypeEnum(row[3]) if row[3] is not None else PermissionTypeEnum.NO_PERMISSION
        categories.append((category, permission))
    return categories