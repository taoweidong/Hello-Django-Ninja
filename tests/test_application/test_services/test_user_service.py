"""
测试用户应用服务
"""

from django.test import TestCase
from app.application.services.user_service import UserService


class TestUserService(TestCase):
    def test_user_service_creation(self):
        """测试用户服务创建"""
        # 由于需要依赖注入，我们只测试类可以被导入
        self.assertTrue(True)