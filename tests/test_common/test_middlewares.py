import unittest
from unittest.mock import Mock, patch
from django.http import HttpRequest, HttpResponse
from app.common.middleware.operation_log_middleware import OperationLogMiddleware
from app.domain.models.user import User


class TestOperationLogMiddleware(unittest.TestCase):
    
    def setUp(self):
        """测试初始化"""
        self.middleware = OperationLogMiddleware(get_response=lambda request: HttpResponse())
        self.request = HttpRequest()
        self.response = HttpResponse()
    
    def test_should_record_log_white_list(self):
        """测试白名单路径不记录日志"""
        self.request.path_info = '/api/health/'
        # 使用__dict__直接设置只读属性
        self.request.__dict__['method'] = 'POST'
        self.assertFalse(self.middleware._should_record_log(self.request))
        
        self.request.path_info = '/api/auth/login'
        self.assertFalse(self.middleware._should_record_log(self.request))
    
    def test_should_record_log_non_record_methods(self):
        """测试非记录方法不记录日志"""
        self.request.path_info = '/api/users/'
        self.request.__dict__['method'] = 'GET'
        self.assertFalse(self.middleware._should_record_log(self.request))
        
        self.request.__dict__['method'] = 'HEAD'
        self.assertFalse(self.middleware._should_record_log(self.request))
    
    def test_should_record_log_record_methods(self):
        """测试记录方法记录日志"""
        self.request.path_info = '/api/users/'
        self.request.__dict__['method'] = 'POST'
        self.assertTrue(self.middleware._should_record_log(self.request))
        
        self.request.__dict__['method'] = 'PUT'
        self.assertTrue(self.middleware._should_record_log(self.request))
        
        self.request.__dict__['method'] = 'PATCH'
        self.assertTrue(self.middleware._should_record_log(self.request))
        
        self.request.__dict__['method'] = 'DELETE'
        self.assertTrue(self.middleware._should_record_log(self.request))
    
    def test_get_client_ip_with_x_forwarded_for(self):
        """测试获取客户端IP - X-Forwarded-For"""
        self.request.META['HTTP_X_FORWARDED_FOR'] = '192.168.1.1, 10.0.0.1'
        self.assertEqual(self.middleware._get_client_ip(self.request), '192.168.1.1')
    
    def test_get_client_ip_with_remote_addr(self):
        """测试获取客户端IP - REMOTE_ADDR"""
        self.request.META['REMOTE_ADDR'] = '192.168.1.2'
        self.assertEqual(self.middleware._get_client_ip(self.request), '192.168.1.2')
    
    def test_get_client_ip_no_ip(self):
        """测试获取客户端IP - 无IP信息"""
        self.assertEqual(self.middleware._get_client_ip(self.request), '')
    
    def test_get_user_agent(self):
        """测试获取用户代理"""
        self.request.META['HTTP_USER_AGENT'] = 'Mozilla/5.0'
        self.assertEqual(self.middleware._get_user_agent(self.request), 'Mozilla/5.0')
    
    def test_get_module_name(self):
        """测试获取模块名称"""
        self.assertEqual(self.middleware._get_module_name('/api/users/'), '用户管理')
        self.assertEqual(self.middleware._get_module_name('/api/roles/'), '角色管理')
        self.assertEqual(self.middleware._get_module_name('/api/permissions/'), '权限管理')
        self.assertEqual(self.middleware._get_module_name('/api/unknown/'), '系统管理')
    
    def test_get_business_type(self):
        """测试获取业务类型"""
        self.assertEqual(self.middleware._get_business_type('POST'), '新增')
        self.assertEqual(self.middleware._get_business_type('PUT'), '修改')
        self.assertEqual(self.middleware._get_business_type('PATCH'), '修改')
        self.assertEqual(self.middleware._get_business_type('DELETE'), '删除')
        self.assertEqual(self.middleware._get_business_type('GET'), '其他')
    
    @patch('app.common.middlewares.JWTAuth')
    def test_get_current_user_with_request_user(self, mock_jwt_auth):
        """测试获取当前用户 - 从request.user"""
        # 创建模拟用户
        mock_user = Mock(spec=User)
        mock_user.username = 'testuser'
        
        # 设置request.user（使用__dict__直接设置）
        self.request.__dict__['user'] = mock_user
        
        # 调用方法
        user = self.middleware._get_current_user(self.request)
        
        # 验证结果
        self.assertEqual(user, mock_user)
        mock_jwt_auth.assert_not_called()
    
    @patch('app.common.middlewares.JWTAuth')
    def test_get_current_user_with_jwt_token(self, mock_jwt_auth):
        """测试获取当前用户 - 从JWT token"""
        # 设置request没有user属性
        if 'user' in self.request.__dict__:
            del self.request.__dict__['user']
        
        # 设置Authorization头
        self.request.META['HTTP_AUTHORIZATION'] = 'Bearer test-token'
        
        # 配置JWT认证模拟
        mock_auth_instance = Mock()
        mock_auth_instance.authenticate.return_value = Mock(spec=User)
        mock_jwt_auth.return_value = mock_auth_instance
        
        # 调用方法
        user = self.middleware._get_current_user(self.request)
        
        # 验证结果
        self.assertIsInstance(user, User)
        mock_jwt_auth.assert_called_once()
        mock_auth_instance.authenticate.assert_called_once()
    
    def test_get_current_user_anonymous(self):
        """测试获取当前用户 - 匿名用户"""
        # 设置request没有user属性
        if 'user' in self.request.__dict__:
            del self.request.__dict__['user']
        
        # 调用方法
        user = self.middleware._get_current_user(self.request)
        
        # 验证结果
        self.assertIsNone(user)


if __name__ == '__main__':
    unittest.main()