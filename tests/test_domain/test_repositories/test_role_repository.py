"""
测试角色仓储接口
"""

from django.test import TestCase
from app.domain.repositories.role_repository import RoleRepository


class TestRoleRepository(TestCase):
    def test_role_repository_is_abstract(self):
        """测试角色仓储接口是抽象的"""
        # 这是一个抽象类，不能直接实例化
        with self.assertRaises(TypeError):
            RoleRepository()