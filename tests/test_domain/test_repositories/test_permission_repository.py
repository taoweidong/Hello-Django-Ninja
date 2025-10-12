"""
测试权限仓储接口
"""

from django.test import TestCase
from app.domain.repositories.permission_repository import PermissionRepository


class TestPermissionRepository(TestCase):
    def test_permission_repository_is_abstract(self):
        """测试权限仓储接口是抽象的"""
        # 这是一个抽象类，不能直接实例化
        with self.assertRaises(TypeError):
            PermissionRepository()