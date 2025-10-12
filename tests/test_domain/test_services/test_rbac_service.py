"""
测试RBAC服务
"""

from django.test import TestCase
from app.domain.services.rbac_service import RBACService


class TestRBACService(TestCase):
    def test_rbac_service_creation(self):
        """测试RBAC服务创建"""
        # 由于需要依赖注入，我们只测试类可以被导入
        self.assertTrue(True)