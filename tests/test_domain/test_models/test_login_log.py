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
        login_time = timezone.now()
        
        login_log = LoginLog(
            id=login_log_id,
            ip_address="192.168.1.1",
            user_agent="Test User Agent",
            login_status=True,
            login_time=login_time,
            user=self.user
        )
        login_log.save()
        
        self.assertEqual(login_log.id, login_log_id)
        self.assertEqual(login_log.ip_address, "192.168.1.1")
        self.assertEqual(login_log.user_agent, "Test User Agent")
        self.assertEqual(login_log.login_status, True)
        self.assertEqual(login_log.login_time, login_time)
        self.assertEqual(login_log.user, self.user)
        
    def test_login_log_str_representation(self):
        """测试登录日志字符串表示"""
        login_time = timezone.now()
        
        login_log = LoginLog(
            id=uuid.uuid4().hex[:32],
            ip_address="192.168.1.1",
            user_agent="Test User Agent",
            login_status=True,
            login_time=login_time,
            user=self.user
        )
        login_log.save()
        
        expected_str = f"LoginLog for user {self.user} at {login_time}"
        self.assertEqual(str(login_log), expected_str)
        
    def test_login_log_with_logout_time(self):
        """测试登录日志带登出时间"""
        login_time = timezone.now()
        logout_time = timezone.now()
        
        login_log = LoginLog(
            id=uuid.uuid4().hex[:32],
            ip_address="192.168.1.1",
            user_agent="Test User Agent",
            login_status=True,
            login_time=login_time,
            logout_time=logout_time,
            user=self.user
        )
        login_log.save()
        
        self.assertEqual(login_log.logout_time, logout_time)