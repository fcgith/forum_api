from typing import List

from models.category import Category, CategoryCreate
import repo.category as category_repo
import repo.topic as topics_repo
from services.errors import not_found, access_denied, invalid_credentials, bad_request
from services.utils import AuthToken


class CategoryService:
    @classmethod
    def get_all(cls,token) -> list[Category]:
        """
        Retrieve all categories from the database.
        """
        AuthToken.validate_admin(token)

        return category_repo.get_all_categories()

    @classmethod
    def get_all_viewable(cls, token: str) -> List[Category]:
        user = AuthToken.validate(token)
        if not user:
            raise invalid_credentials
        return category_repo.get_all_viewable_categories(user)

    @classmethod
    def get_by_id(cls, category_id: int,token: str) -> Category:
        """
        Retrieve a specific category by ID.

        :param category_id: ID of the category.
        :param token: Authentication token for user validation.
        :return: Category object or raise 404 if not found.
        """
        user = AuthToken.validate(token)
        if not user:
            raise invalid_credentials
        if not category_repo.is_category_viewable(category_id, user.id):
            raise access_denied
        category = category_repo.get_category_by_id(category_id)
        if not category:
            raise not_found
        return category

    @classmethod
    def create(cls, data: CategoryCreate,token: str) -> int:
        """
        Create a new category in the system.

        :param data: Data for the new category.
        :param token: Authentication token for user validation.
        :return: ID of the created category.
        """
        AuthToken.validate_admin(token)

        return category_repo.create_category(data)

    @classmethod
    def get_topics_by_category_id(cls, category_id: int, token: str):
        user = AuthToken.validate(token)
        if not user:
            raise invalid_credentials

        if not category_repo.is_category_viewable(category_id, user.id):
            raise access_denied

        return topics_repo.get_topics_in_category(category_id)

    @classmethod
    def update_hidden_status(cls, category_id: int, hidden: int, token: str):
        AuthToken.validate_admin(token)

        category = category_repo.get_category_by_id(category_id)

        if not category:
            raise not_found

        if hidden not in (0, 1):
            raise bad_request

        return category_repo.update_hidden_status(category_id, hidden)