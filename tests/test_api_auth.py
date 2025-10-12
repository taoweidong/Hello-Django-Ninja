"""
API 认证和权限测试
"""

import pytest
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
import json

User = get_user_model()


@pytest.mark.django_db
class APITestCase(TestCase):
    def setUp(self):
        # 创建测试用户
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )
        self.client = Client()
    
    def test_auth_controller_login(self):
        # 测试登录接口
        response = self.client.post('/api/auth/login', 
            data=json.dumps({
                "username": "testuser",
                "password": "testpass123"
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content.decode('utf-8'))
        self.assertIn("token", data)
    
    def test_auth_controller_login_invalid(self):
        # 测试无效登录
        response = self.client.post('/api/auth/login', 
            data=json.dumps({
                "username": "testuser",
                "password": "wrongpass"
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 401)
    
    def test_users_list_unauthorized(self):
        # 测试未认证访问用户列表
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, 401)
    
    def test_health_check(self):
        # 测试健康检查接口（不需要认证）
        response = self.client.get('/api/health/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(data["status"], "healthy")