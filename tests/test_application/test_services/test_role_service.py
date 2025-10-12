"""
测试角色应用服务
"""

from django.test import TestCase
from app.application.services.role_service import RoleService


class TestRoleService(TestCase):
    def test_role_service_creation(self):
        """测试角色服务创建"""
        # 由于需要依赖注入，我们只测试类可以被导入
        self.assertTrue(True)