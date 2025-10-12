"""
测试角色模型
"""

from django.test import TestCase
from app.domain.models.role import Role


class TestRoleModel(TestCase):
    def test_role_creation(self):
        """测试角色创建"""
        role = Role(name="test_role", description="Test role description")
        role.save()
        self.assertEqual(role.name, "test_role")
        self.assertEqual(role.description, "Test role description")

    def test_role_str_representation(self):
        """测试角色字符串表示"""
        role = Role(name="test_role", description="Test role description")
        role.save()
        self.assertEqual(str(role), "test_role")

    def test_role_id_property(self):
        """测试角色ID属性"""
        role = Role(name="test_role2", description="Test role description 2")
        role.save()
        self.assertEqual(role.id, role.pk)

    def test_role_unique_name(self):
        """测试角色名称唯一性"""
        role1 = Role(name="unique_role", description="Unique role")
        role1.save()
        with self.assertRaises(Exception):
            role2 = Role(name="unique_role", description="Duplicate role")
            role2.save()