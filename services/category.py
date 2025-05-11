from typing import List

from models.category import Category, CategoryCreate
import repo.category as category_repo
from services.errors import not_found, access_denied, invalid_credentials
from services.utils import AuthToken


class CategoryService:
    @classmethod
    def get_all(cls) -> list[Category]:
        """
        Retrieve all categories from the database.
        """
        return category_repo.get_all_categories()

    @classmethod
    def get_all_viewable(self, token: str) -> List[Category]:
        user = AuthToken.validate(token)
        if not user:
            raise invalid_credentials
        return category_repo.get_all_viewable_categories(user)

    @classmethod
    def get_by_id(cls, category_id: int) -> Category:
        """
        Retrieve a specific category by ID.

        :param category_id: ID of the category.
        :return: Category object or raise 404 if not found.
        """
        category = category_repo.get_category_by_id(category_id)
        if not category:
            raise not_found
        return category

    @classmethod
    def create(cls, data: CategoryCreate) -> int:
        """
        Create a new category in the system.

        :param data: Data for the new category.
        :return: ID of the created category.
        """
        return category_repo.create_category(data)