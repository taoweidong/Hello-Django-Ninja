"""
测试项目基本功能
"""

import pytest
from django.test import TestCase
from django.contrib.auth import get_user_model


@pytest.mark.django_db
class TestUserModel(TestCase):
    def test_create_user(self):
        """测试创建用户"""
        User = get_user_model()
        user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("testpass123"))
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_active)

    def test_create_superuser(self):
        """测试创建超级用户"""
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            username="admin", email="admin@example.com", password="adminpass123"
        )
        self.assertEqual(admin_user.username, "admin")
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
