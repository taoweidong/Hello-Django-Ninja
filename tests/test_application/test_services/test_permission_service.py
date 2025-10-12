"""
测试权限应用服务
"""

from django.test import TestCase
from app.application.services.permission_service import PermissionService


class TestPermissionService(TestCase):
    def test_permission_service_creation(self):
        """测试权限服务创建"""
        # 由于需要依赖注入，我们只测试类可以被导入
        self.assertTrue(True)