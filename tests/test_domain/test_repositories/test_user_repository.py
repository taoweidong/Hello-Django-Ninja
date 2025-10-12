"""
测试用户仓储接口
"""

from django.test import TestCase
from app.domain.repositories.user_repository import UserRepository


class TestUserRepository(TestCase):
    def test_user_repository_is_abstract(self):
        """测试用户仓储接口是抽象的"""
        # 这是一个抽象类，不能直接实例化
        with self.assertRaises(TypeError):
            UserRepository()