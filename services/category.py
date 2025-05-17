from typing import List

from models.category import Category, CategoryCreate
import repo.category as category_repo
import repo.topic as topics_repo
import repo.user as user_repo
from services.errors import not_found, access_denied, bad_request, category_not_found, user_not_found
from services.utils import AuthToken


class CategoryService:
    @classmethod
    def get_all(cls, token) -> list[Category]:
        """
        Retrieve all categories from the database.
        """
        AuthToken.validate_admin(token)

        return category_repo.get_all_categories()

    @classmethod
    def get_all_viewable(cls, token: str) -> List[Category]:
        # TODO: docstring
        user = AuthToken.validate(token)
        return category_repo.get_all_viewable_categories(user)

    @classmethod
    def get_by_id(cls, category_id: int, token: str) -> Category:
        """
        Retrieve a specific category by ID.

        :param category_id: ID of the category.
        :param token: Authentication token for user validation.
        :return: Category object or raise 404 if not found.
        """
        user = AuthToken.validate(token)

        if not category_repo.check_category_read_permission(category_id, user):
            raise access_denied

        category = category_repo.get_category_by_id(category_id)
        if not category:
            raise not_found

        return category

    @classmethod
    def create(cls, data: CategoryCreate, token: str) -> int:
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
        # TODO: docstring
        user = AuthToken.validate(token)

        if not category_repo.check_category_read_permission(category_id, user):
            raise access_denied

        return topics_repo.get_topics_in_category(category_id)

    @classmethod
    def update_hidden_status(cls, category_id: int, hidden: int, token: str) -> dict:
        """
        Changes category hidden status if the user is admin or raises an error.
        """
        AuthToken.validate_admin(token)

        category = category_repo.get_category_by_id(category_id)

        if not category:
            raise category_not_found

        if hidden not in (0, 1):
            raise bad_request

        return category_repo.update_hidden_status(category_id, hidden)

    @classmethod
    def update_user_permissions(cls, category_id: int,
                                user_id: int,
                                permission: int,
                                token: str) -> dict:
        """
        Updates the permission level of a user for a category.
        """
        AuthToken.validate_admin(token)
        if permission not in (0, 1, 2, 3):
            raise bad_request

        category = category_repo.get_category_by_id(category_id)
        if not category:
            raise category_not_found

        user = user_repo.get_user_by_id(user_id)
        if not user:
            raise user_not_found

        return category_repo.update_permissions(category_id, user_id, permission)

    # TODO: duplicate function with update_hidden_status
    # @classmethod
    # def hide_category_by_id(cls, category_id, token) -> bool:
    #     AuthToken.validate_admin(token)
    #
    #     category = cls.get_by_id(category_id, token)
    #     if not category:
    #         raise category_not_found
    #
    #     return category_repo.hide_category(category_id)
    @classmethod
    def get_read_or_write_permission(cls, category_id, token):
        user = AuthToken.validate(token)
        if user.is_admin():
            return "write_access"
        perm = category_repo.get_user_category_permission(category_id, user)
        match perm:
            case 0:
                return "no_access"
            case 1:
                return "normal_access"
            case 2:
                return "read_only_access"
            case 3:
                return "write_access"
            case _:
                return "no_access"

    @classmethod
    def category_lock(cls, category_id, token) -> dict:
        AuthToken.validate_admin(token)
        category = category_repo.get_category_by_id(category_id)
        if not category:
            raise category_not_found
        return category_repo.update_locked_status(category_id)
