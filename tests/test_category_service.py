import unittest
from unittest.mock import patch, MagicMock
from services.category import CategoryService
from services.errors import not_found, access_denied, bad_request, category_not_found

class TestCategoryService(unittest.TestCase):
    def setUp(self):
        self.token = "mocked_token"
        self.user = MagicMock(id=1, is_admin=MagicMock(return_value=False))
        self.admin_user = MagicMock(id=99, is_admin=MagicMock(return_value=True))
        self.mock_category = MagicMock(id=1, locked=0)
        self.mock_user = MagicMock(id=2)

    @patch("services.category.AuthToken.validate_admin")
    @patch("services.category.category_repo.get_all_categories")
    def test_get_all(self, mock_get_all_categories, mock_validate_admin):
        mock_validate_admin.return_value = self.admin_user
        mock_get_all_categories.return_value = [self.mock_category]
        result = CategoryService.get_all(self.token)
        self.assertEqual(result, [self.mock_category])

    @patch("services.category.AuthToken.validate")
    @patch("services.category.category_repo.get_all_viewable_categories")
    def test_get_all_viewable(self, mock_get_all_viewable, mock_validate):
        mock_validate.return_value = self.user
        mock_get_all_viewable.return_value = [self.mock_category]
        result = CategoryService.get_all_viewable(self.token)
        self.assertEqual(result, [self.mock_category])

    @patch("services.category.AuthToken.validate")
    @patch("services.category.category_repo.check_category_read_permission")
    @patch("services.category.category_repo.get_category_by_id")
    def test_get_by_id_success(self, mock_get_cat, mock_check_perm, mock_validate):
        mock_validate.return_value = self.user
        mock_check_perm.return_value = True
        mock_get_cat.return_value = self.mock_category
        result = CategoryService.get_by_id(1, self.token)
        self.assertEqual(result, self.mock_category)

    @patch("services.category.AuthToken.validate")
    @patch("services.category.category_repo.check_category_read_permission")
    def test_get_by_id_access_denied(self, mock_check_perm, mock_validate):
        mock_validate.return_value = self.user
        mock_check_perm.return_value = False
        with self.assertRaises(type(access_denied)):
            CategoryService.get_by_id(1, self.token)

    @patch("services.category.AuthToken.validate")
    @patch("services.category.category_repo.check_category_read_permission")
    @patch("services.category.category_repo.get_category_by_id")
    def test_get_by_id_not_found(self, mock_get_cat, mock_check_perm, mock_validate):
        mock_validate.return_value = self.user
        mock_check_perm.return_value = True
        mock_get_cat.return_value = None
        with self.assertRaises(type(not_found)):
            CategoryService.get_by_id(1, self.token)

    @patch("services.category.AuthToken.validate_admin")
    @patch("services.category.category_repo.create_category")
    def test_create_success(self, mock_create_category, mock_validate_admin):
        mock_validate_admin.return_value = self.admin_user
        mock_create_category.return_value = 10
        data = MagicMock()
        result = CategoryService.create(data, self.token)
        self.assertEqual(result, 10)

    @patch("services.category.AuthToken.validate")
    @patch("services.category.category_repo.check_category_read_permission")
    @patch("services.category.topics_repo.get_topics_in_category")
    def test_get_topics_by_category_id_success(self, mock_get_topics, mock_check_perm, mock_validate):
        mock_validate.return_value = self.user
        mock_check_perm.return_value = True
        mock_get_topics.return_value = [MagicMock(id=1)]
        result = CategoryService.get_topics_by_category_id(1, self.token)
        self.assertEqual(result[0].id, 1)

    @patch("services.category.AuthToken.validate")
    @patch("services.category.category_repo.check_category_read_permission")
    def test_get_topics_by_category_id_access_denied(self, mock_check_perm, mock_validate):
        mock_validate.return_value = self.user
        mock_check_perm.return_value = False
        with self.assertRaises(type(access_denied)):
            CategoryService.get_topics_by_category_id(1, self.token)

    @patch("services.category.AuthToken.validate_admin")
    @patch("services.category.category_repo.get_category_by_id")
    @patch("services.category.category_repo.update_hidden_status")
    def test_update_hidden_status_success(self, mock_update_hidden, mock_get_cat, mock_validate_admin):
        mock_validate_admin.return_value = self.admin_user
        mock_get_cat.return_value = self.mock_category
        mock_update_hidden.return_value = True
        result = CategoryService.update_hidden_status(1, 1, self.token)
        self.assertTrue(result)

    @patch("services.category.AuthToken.validate_admin")
    @patch("services.category.category_repo.get_category_by_id")
    def test_update_hidden_status_not_found(self, mock_get_cat, mock_validate_admin):
        mock_validate_admin.return_value = self.admin_user
        mock_get_cat.return_value = None
        with self.assertRaises(type(not_found)):
            CategoryService.update_hidden_status(1, 1, self.token)

    @patch("services.category.AuthToken.validate_admin")
    @patch("services.category.category_repo.get_category_by_id")
    def test_update_hidden_status_bad_request(self, mock_get_cat, mock_validate_admin):
        mock_validate_admin.return_value = self.admin_user
        mock_get_cat.return_value = self.mock_category
        with self.assertRaises(type(bad_request)):
            CategoryService.update_hidden_status(1, 5, self.token)

    @patch("services.category.AuthToken.validate_admin")
    @patch("services.category.category_repo.get_category_by_id")
    @patch("services.category.user_repo.get_user_by_id")
    @patch("services.category.category_repo.update_permissions")
    def test_update_user_permissions_success(self, mock_update_perms, mock_get_user, mock_get_cat, mock_validate_admin):
        mock_validate_admin.return_value = self.admin_user
        mock_get_cat.return_value = self.mock_category
        mock_get_user.return_value = self.mock_user
        mock_update_perms.return_value = True
        result = CategoryService.update_user_permissions(1, 2, 3, self.token)
        self.assertTrue(result)

    @patch("services.category.AuthToken.validate_admin")
    @patch("services.category.category_repo.get_category_by_id")
    @patch("services.category.user_repo.get_user_by_id")
    def test_update_user_permissions_not_found(self, mock_get_user, mock_get_cat, mock_validate_admin):
        mock_validate_admin.return_value = self.admin_user
        mock_get_cat.return_value = None
        mock_get_user.return_value = None
        with self.assertRaises(type(not_found)):
            CategoryService.update_user_permissions(1, 2, 3, self.token)

    @patch("services.category.AuthToken.validate_admin")
    @patch("services.category.category_repo.get_category_by_id")
    @patch("services.category.user_repo.get_user_by_id")
    def test_update_user_permissions_bad_request(self, mock_get_user, mock_get_cat, mock_validate_admin):
        mock_validate_admin.return_value = self.admin_user
        mock_get_cat.return_value = self.mock_category
        mock_get_user.return_value = self.mock_user
        with self.assertRaises(type(bad_request)):
            CategoryService.update_user_permissions(1, 2, 99, self.token)

    @patch("services.category.AuthToken.validate")
    @patch("services.category.category_repo.get_user_category_permission")
    def test_get_read_or_write_permission_admin(self, mock_get_perm, mock_validate):
        mock_validate.return_value = self.admin_user
        self.admin_user.is_admin.return_value = True
        result = CategoryService.get_read_or_write_permission(1, self.token)
        self.assertEqual(result, "write_access")

    @patch("services.category.AuthToken.validate")
    @patch("services.category.category_repo.get_user_category_permission")
    def test_get_read_or_write_permission_normal(self, mock_get_perm, mock_validate):
        mock_validate.return_value = self.user
        self.user.is_admin.return_value = False
        mock_get_perm.return_value = 1
        result = CategoryService.get_read_or_write_permission(1, self.token)
        self.assertEqual(result, "normal_access")

    @patch("services.category.AuthToken.validate_admin")
    @patch("services.category.category_repo.get_category_by_id")
    @patch("services.category.category_repo.update_locked_status")
    def test_category_lock_success(self, mock_update_locked, mock_get_cat, mock_validate_admin):
        mock_validate_admin.return_value = self.admin_user
        mock_get_cat.return_value = self.mock_category
        mock_update_locked.return_value = True
        result = CategoryService.category_lock(1, self.token)
        self.assertTrue(result)

    @patch("services.category.AuthToken.validate_admin")
    @patch("services.category.category_repo.get_category_by_id")
    def test_category_lock_not_found(self, mock_get_cat, mock_validate_admin):
        mock_validate_admin.return_value = self.admin_user
        mock_get_cat.return_value = None
        with self.assertRaises(type(category_not_found)):
            CategoryService.category_lock(1, self.token)

if __name__ == "__main__":
    unittest.main()
