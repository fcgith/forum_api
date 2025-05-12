from typing import List, Tuple
from models.category import Category, CategoryCreate
from models.category_permission import PermissionTypeEnum
from data.connection import read_query, insert_query, update_query
from models.topic import Topic
from models.user import User
from repo.topic import gen_topic
from services.errors import not_found, category_not_found
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
    placeholder = get_viewable_category_ids(user.id)
    placeholder = [str(id) for id in placeholder]
    query = f"SELECT * FROM categories WHERE id IN ({", ".join(placeholder)})"
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

def get_categories_with_permissions(user_id: int) -> List[Tuple[Category, PermissionTypeEnum]]:
    query = "SELECT c.id, c.name, c.description, cp.type FROM categories c LEFT JOIN category_permissions cp ON c.id = cp.category_id AND cp.user_id = ?"
    result = read_query(query, (user_id,))
    categories = []
    for row in result:
        category = Category(id=row[0], name=row[1], description=row[2])
        permission = PermissionTypeEnum(row[3]) if row[3] is not None else PermissionTypeEnum.NO_PERMISSION
        categories.append((category, permission))
    return categories

def get_all_category_ids() -> List[int]:
    query = "SELECT id FROM categories"
    return [row[0] for row in read_query(query)]

def get_category_permissions(category_id: int, user_id: int) -> int:
    query = "SELECT type FROM category_permissions WHERE category_id = ? AND user_id = ?"
    result = read_query(query, (category_id, user_id))

    return 1 if not result else result[0][0] # 1 = Default

def is_category_viewable(category_id: int, user_id: int) -> bool:
    perm = get_category_permissions(category_id, user_id)
    user = user_repo.get_user_by_id(user_id)

    if user.is_admin():
        return True

    if perm == 0:
        return False # no permission at all

    query = "SELECT hidden FROM categories WHERE id = ?"
    result = read_query(query, (category_id,))

    if result:
        ctype = result[0][0] # 0 for hidden, 1 for viewable
    else:
        raise category_not_found # category not found

    if ctype == 1:
        # hidden category
        return perm >= 2
    elif ctype == 0:
        # public category
        return perm >= 1
    else:
        return False

def get_viewable_category_ids(user_id: int) -> List[int]:
    category_ids = get_all_category_ids()
    return [
        category_id
        for category_id in category_ids
        if is_category_viewable(category_id, user_id)
    ]

def set_category_permissions(category_id: int, user_id: int, permission: int) -> bool:
    query = "SELECT * FROM category_permissions WHERE category_id = ? AND user_id = ?"
    result = read_query(query, (category_id, user_id))

    if not result:
        query = "INSERT INTO category_permissions (category_id, user_id, type) VALUES (?, ?, ?)"
        result = insert_query(query, (category_id, user_id, permission))
    else:
        query = "UPDATE category_permissions SET type = ? WHERE category_id = ? AND user_id = ?"
        result = update_query(query, (permission, category_id, user_id))

    return True if result else False


def get_topics_in_category(category_id) -> List[Topic] | []:
    query = "SELECT * FROM topics WHERE category_id = ? ORDER BY id DESC"
    result = read_query(query, (category_id,))
    return [gen_topic(row) for row in result] if result else []