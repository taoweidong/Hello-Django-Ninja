"""
测试用户模型
"""

from django.test import TestCase
from app.domain.models.user import User


class TestUserModel(TestCase):
    def test_user_creation(self):
        """测试用户创建"""
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("testpass123"))
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_active)

    def test_superuser_creation(self):
        """测试超级用户创建"""
        admin_user = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="adminpass123"
        )
        self.assertEqual(admin_user.username, "admin")
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.check_password("adminpass123"))

    def test_user_id_property(self):
        """测试用户ID属性"""
        user = User.objects.create_user(
            username="testuser2",
            email="test2@example.com",
            password="testpass123"
        )
        self.assertEqual(user.id, user.pk)