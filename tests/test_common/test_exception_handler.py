"""
测试全局异常处理器
"""

from unittest.mock import Mock
from django.test import TestCase
from ninja_extra import ControllerBase
from ninja_extra.exceptions import APIException

from app.common.exception.exception_handler import global_exception_handler
from app.common.exception.exceptions import (
    BusinessException,
    NotFoundException,
    ValidationException,
    PermissionDeniedException,
    InvalidRoleAssignmentException,
)
from app.common.api_response import ApiResponse


class TestGlobalExceptionHandler(TestCase):
    def setUp(self):
        """设置测试环境"""
        self.controller = Mock(spec=ControllerBase)
        self.controller.create_response = Mock()
        
        # 模拟create_response方法的行为
        def create_response_side_effect(message, status_code, **kwargs):
            # 返回一个模拟的HttpResponse对象
            response = Mock()
            response.status_code = status_code
            response.message = message
            return response
            
        self.controller.create_response.side_effect = create_response_side_effect

    def test_business_exception_handling(self):
        """测试业务异常处理"""
        exception = BusinessException("Business error")
        result = global_exception_handler(self.controller, exception)
        
        # 验证create_response被正确调用
        self.controller.create_response.assert_called_once()
        args, kwargs = self.controller.create_response.call_args
        self.assertEqual(kwargs['status_code'], 400)
        self.assertIsInstance(args[0], ApiResponse)
        self.assertEqual(args[0].code, 400)
        self.assertEqual(args[0].message, "Business error")

    def test_not_found_exception_handling(self):
        """测试未找到异常处理"""
        exception = NotFoundException("Resource not found")
        result = global_exception_handler(self.controller, exception)
        
        # 验证create_response被正确调用
        self.controller.create_response.assert_called_once()
        args, kwargs = self.controller.create_response.call_args
        self.assertEqual(kwargs['status_code'], 404)
        self.assertIsInstance(args[0], ApiResponse)
        self.assertEqual(args[0].code, 404)
        self.assertEqual(args[0].message, "Resource not found")

    def test_validation_exception_handling(self):
        """测试验证异常处理"""
        exception = ValidationException("Validation failed")
        result = global_exception_handler(self.controller, exception)
        
        # 验证create_response被正确调用
        self.controller.create_response.assert_called_once()
        args, kwargs = self.controller.create_response.call_args
        self.assertEqual(kwargs['status_code'], 400)
        self.assertIsInstance(args[0], ApiResponse)
        self.assertEqual(args[0].code, 400)
        self.assertEqual(args[0].message, "Validation failed")

    def test_permission_denied_exception_handling(self):
        """测试权限拒绝异常处理"""
        exception = PermissionDeniedException("Permission denied")
        result = global_exception_handler(self.controller, exception)
        
        # 验证create_response被正确调用
        self.controller.create_response.assert_called_once()
        args, kwargs = self.controller.create_response.call_args
        self.assertEqual(kwargs['status_code'], 403)
        self.assertIsInstance(args[0], ApiResponse)
        self.assertEqual(args[0].code, 403)
        self.assertEqual(args[0].message, "Permission denied")

    def test_invalid_role_assignment_exception_handling(self):
        """测试无效角色分配异常处理"""
        exception = InvalidRoleAssignmentException("Invalid role assignment")
        result = global_exception_handler(self.controller, exception)
        
        # 验证create_response被正确调用
        self.controller.create_response.assert_called_once()
        args, kwargs = self.controller.create_response.call_args
        self.assertEqual(kwargs['status_code'], 400)
        self.assertIsInstance(args[0], ApiResponse)
        self.assertEqual(args[0].code, 400)
        self.assertEqual(args[0].message, "Invalid role assignment")

    def test_api_exception_handling(self):
        """测试API异常处理"""
        exception = APIException("API error", 422)
        result = global_exception_handler(self.controller, exception)
        
        # 验证create_response被正确调用
        self.controller.create_response.assert_called_once()
        args, kwargs = self.controller.create_response.call_args
        self.assertEqual(kwargs['status_code'], 422)
        self.assertIsInstance(args[0], ApiResponse)
        self.assertEqual(args[0].code, 422)
        self.assertEqual(args[0].message, "API error")

    def test_generic_exception_handling(self):
        """测试通用异常处理"""
        exception = Exception("Generic error")
        result = global_exception_handler(self.controller, exception)
        
        # 验证create_response被正确调用
        self.controller.create_response.assert_called_once()
        args, kwargs = self.controller.create_response.call_args
        self.assertEqual(kwargs['status_code'], 500)
        self.assertIsInstance(args[0], ApiResponse)
        self.assertEqual(args[0].code, 500)
        self.assertEqual(args[0].message, "Internal server error")