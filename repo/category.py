from typing import List, Tuple
from models.category import Category, CategoryCreate
from models.category_permission import PermissionTypeEnum
from data.connection import read_query, insert_query, update_query
from models.topic import Topic
from models.user import User
from services.errors import not_found, category_not_found, bad_request
from repo import topic as topics_repo
from repo import user as user_repo

def gen_category(result: tuple) -> Category:
    return Category(
        id=result[0],
        name=result[1],
        description=result[2],
        hidden=result[3],
        topics_count=topics_repo.get_topics_count_by_category(result[0])
    )

def get_all_categories() -> List[Category] | None:
    query = "SELECT * FROM categories"
    result = read_query(query)
    if result:
        return [gen_category(row) for row in result]
    return []

def get_all_viewable_categories(user: User) -> List[Category]:
    viewable_ids = get_viewable_category_ids(user)
    viewable_ids = ", ".join([str(id) for id in viewable_ids])
    query = f"SELECT * FROM categories WHERE id IN ({viewable_ids}) ORDER BY name ASC"
    result = read_query(query)
    if not result:
        return []
    return [gen_category(row) for row in result]

def get_category_by_id(category_id: int) -> Category | None:
    query = "SELECT * FROM categories WHERE id = ?"
    result = read_query(query, (category_id,))
    if result:
        return gen_category(result[0])
    return None

def create_category(data: CategoryCreate) -> int | None:
    query = "INSERT INTO categories (name, description) VALUES (?, ?)"
    return insert_query(query, (data.name, data.description))

def check_category_write_permission(category_id: int, user: User) -> bool:
    if user.is_admin():
        return True

    category = get_category_by_id(category_id)

    if not category:
        raise category_not_found

    if category.hidden == 0:
        return True
    else:
        perm = get_user_category_permission(category_id, user)
        return perm >= 3

def check_category_read_permission(category_id: int, user: User) -> bool:
    if user.is_admin():
        return True

    category = get_category_by_id(category_id)

    if not category:
        raise category_not_found

    if category.hidden == 0:
        return True
    else:
        perm = get_user_category_permission(category_id, user)

        if perm == 0:
            return False # no permission at all

        return perm >= 2


def get_viewable_category_ids(user: User) -> List[int]:
    category_ids = get_all_category_ids()
    return [
        category_id
        for category_id in category_ids
        if check_category_read_permission(category_id, user)
    ]

# def get_categories_with_permissions(user: User) -> List[dict]:
#     # TODO: Not used and not really useful
#     query = "SELECT c.id, c.name, c.description, cp.type FROM categories c LEFT JOIN category_permissions cp ON c.id = cp.category_id AND cp.user_id = ?"
#     result = read_query(query, (user,))
#     categories = [{"category": Category(id=row[0], name=row[1], description=row[2]),
#                    "permission": row[3]}
#                     for row in result]
#
#     return categories

def get_all_category_ids() -> List[int]:
    query = "SELECT id FROM categories"
    return [row[0] for row in read_query(query)]

def get_user_category_permission(category_id: int, user: User) -> int:
    query = "SELECT type FROM category_permissions WHERE category_id = ? AND user_id = ?"
    result = read_query(query, (category_id, user.id))
    return 1 if len(result) == 0 else result[0][0] # 1 = Default

def update_hidden_status(category_id: int, hidden: int) -> bool:
    query = "UPDATE categories SET hidden = ? WHERE id = ?"
    result = update_query(query, (hidden, category_id))
    return True if result else False

def update_permissions(category_id: int, user_id: int, permission: int) -> bool:
    query = "SELECT * FROM category_permissions WHERE category_id = ? AND user_id = ?"
    result = read_query(query, (category_id, user_id))
    if not result:
        query = "INSERT INTO category_permissions (category_id, user_id, type) VALUES (?, ?, ?)"
        result = insert_query(query, (category_id, user_id, permission))
    else:
        query = "UPDATE category_permissions SET type = ? WHERE category_id = ? AND user_id = ?"
        result = update_query(query, (permission, category_id, user_id))
    return True if result > 0 else False

# def hide_category(category_id) -> bool:
#     # TODO: duplicate with update_hidden_status
#     query = "UPDATE categories SET hidden = 1 WHERE id = ?"
#     result = update_query(query, (category_id,))
#     return True if result > 0 else False
def get_privileged_users(category_id):
    query = "SELECT * FROM category_permissions WHERE category_id = ?"
    result = read_query(query, (category_id,))
    users = [[row[2], row[3], row[1]] for row in result]
    return users