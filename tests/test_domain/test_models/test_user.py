"""
测试用户模型
"""

from django.test import TestCase
from app.domain.models.user import User
import uuid


class TestUserModel(TestCase):
    def test_user_creation(self):
        """测试用户创建"""
        # 使用唯一用户名避免冲突
        unique_username = f"testuser_{uuid.uuid4().hex[:8]}"
        user = User.objects.create_user(
            username=unique_username,
            email="test@example.com",
            password="testpass123"
        )
        self.assertEqual(user.username, unique_username)
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("testpass123"))
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_active)

    def test_superuser_creation(self):
        """测试超级用户创建"""
        # 使用唯一用户名避免冲突
        unique_admin_username = f"admin_{uuid.uuid4().hex[:8]}"
        admin_user = User.objects.create_superuser(
            username=unique_admin_username,
            email="admin@example.com",
            password="adminpass123"
        )
        self.assertEqual(admin_user.username, unique_admin_username)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.check_password("adminpass123"))

    def test_user_id_property(self):
        """测试用户ID属性"""
        # 使用唯一用户名避免冲突
        unique_username = f"testuser2_{uuid.uuid4().hex[:8]}"
        user = User.objects.create_user(
            username=unique_username,
            email="test2@example.com",
            password="testpass123"
        )
        self.assertEqual(user.id, user.pk)