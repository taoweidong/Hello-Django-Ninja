"""
测试通用异常处理
"""

from django.test import TestCase
from app.common.exceptions import (
    BusinessException,
    NotFoundException,
    ValidationException,
    PermissionDeniedException,
    InvalidRoleAssignmentException,
)


class TestExceptions(TestCase):
    def test_business_exception(self):
        """测试业务异常"""
        exception = BusinessException("Test business exception")
        self.assertEqual(str(exception), "Test business exception")

    def test_not_found_exception(self):
        """测试未找到异常"""
        exception = NotFoundException("Test not found exception")
        self.assertEqual(str(exception), "Test not found exception")
        self.assertIsInstance(exception, BusinessException)

    def test_validation_exception(self):
        """测试验证异常"""
        exception = ValidationException("Test validation exception")
        self.assertEqual(str(exception), "Test validation exception")
        self.assertIsInstance(exception, BusinessException)

    def test_permission_denied_exception(self):
        """测试权限拒绝异常"""
        exception = PermissionDeniedException("Test permission denied exception")
        self.assertEqual(str(exception), "Test permission denied exception")
        self.assertIsInstance(exception, BusinessException)

    def test_invalid_role_assignment_exception(self):
        """测试无效角色分配异常"""
        exception = InvalidRoleAssignmentException("Test invalid role assignment exception")
        self.assertEqual(str(exception), "Test invalid role assignment exception")
        self.assertIsInstance(exception, BusinessException)