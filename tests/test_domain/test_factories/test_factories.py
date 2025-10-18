"""
测试领域对象工厂
"""

from django.test import TestCase
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from app.domain.factories import UserFactory, RoleFactory, PermissionFactory
from app.domain.models.user import User
from app.domain.models.role import Role
import uuid


class TestUserFactory(TestCase):
    def test_create_user(self):
        """测试创建用户"""
        username = f"testuser_{uuid.uuid4().hex[:8]}"
        email = "test@example.com"
        password = "testpass123"
        
        user = UserFactory.create_user(username, email, password)
        
        self.assertIsInstance(user, User)
        self.assertEqual(user.username, username)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        
        
class TestRoleFactory(TestCase):
    def test_create_role(self):
        """测试创建角色"""
        name = "test_role"
        description = "Test role description"
        
        role = RoleFactory.create_role(name, description)
        
        self.assertIsInstance(role, Role)
        self.assertEqual(role.name, name)
        self.assertEqual(role.description, description)
        
    def test_create_role_without_description(self):
        """测试创建角色（无描述）"""
        name = "test_role"
        
        role = RoleFactory.create_role(name)
        
        self.assertIsInstance(role, Role)
        self.assertEqual(role.name, name)
        self.assertEqual(role.description, "")


class TestPermissionFactory(TestCase):
    def test_create_permission(self):
        """测试创建权限"""
        name = "test_permission"
        codename = "test_codename"
        
        # 创建一个内容类型用于测试
        content_type = ContentType.objects.create(
            app_label='test',
            model='testmodel'
        )
        
        permission = PermissionFactory.create_permission(name, codename, content_type)
        
        self.assertIsInstance(permission, Permission)
        self.assertEqual(permission.name, name)
        self.assertEqual(permission.codename, codename)
        self.assertEqual(permission.content_type, content_type)