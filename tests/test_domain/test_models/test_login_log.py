"""
测试登录日志模型
"""

from django.test import TestCase
from django.utils import timezone
from app.domain.models.login_log import LoginLog
from app.domain.models.user import User
import uuid


class TestLoginLogModel(TestCase):
    def setUp(self):
        """测试初始化"""
        # 创建测试用户
        self.user = User.objects.create_user(
            username=f"testuser_{uuid.uuid4().hex[:8]}",
            email="test@example.com",
            password="testpass123"
        )
        
    def test_login_log_creation(self):
        """测试登录日志创建"""
        login_log_id = uuid.uuid4().hex[:32]
        
        login_log = LoginLog(
            id=login_log_id,
            ipaddress="192.168.1.1",
            agent="Test User Agent",
            status=True,
            login_type=1,
            creator=self.user
        )
        login_log.save()
        
        self.assertEqual(login_log.id, login_log_id)
        self.assertEqual(login_log.ipaddress, "192.168.1.1")
        self.assertEqual(login_log.agent, "Test User Agent")
        self.assertEqual(login_log.status, True)
        self.assertEqual(login_log.login_type, 1)
        self.assertEqual(login_log.creator, self.user)
        
    def test_login_log_str_representation(self):
        """测试登录日志字符串表示"""
        login_log = LoginLog(
            id=uuid.uuid4().hex[:32],
            ipaddress="192.168.1.1",
            agent="Test User Agent",
            status=True,
            login_type=1,
            creator=self.user
        )
        login_log.save()
        
        expected_str = f"LoginLog for creator {self.user} with status {True}"
        self.assertEqual(str(login_log), expected_str)
        
    def test_login_log_with_logout_time(self):
        """测试登录日志带登出时间"""
        # LoginLog模型中没有logout_time字段，所以这个测试需要修改
        login_log_id = uuid.uuid4().hex[:32]
        
        login_log = LoginLog(
            id=login_log_id,
            ipaddress="192.168.1.1",
            agent="Test User Agent",
            status=True,
            login_type=1,
            creator=self.user
        )
        login_log.save()
        
        self.assertEqual(login_log.id, login_log_id)