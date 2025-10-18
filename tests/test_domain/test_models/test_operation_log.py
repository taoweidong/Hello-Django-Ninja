"""
测试操作日志模型
"""

from django.test import TestCase
from app.domain.models.operation_log import OperationLog
from app.domain.models.user import User
import uuid


class TestOperationLogModel(TestCase):
    def setUp(self):
        """测试初始化"""
        # 创建测试用户
        self.user = User.objects.create_user(
            username=f"testuser_{uuid.uuid4().hex[:8]}",
            email="test@example.com",
            password="testpass123"
        )
        
    def test_operation_log_creation(self):
        """测试操作日志创建"""
        operation_log_id = uuid.uuid4().hex[:32]
        
        operation_log = OperationLog(
            id=operation_log_id,
            module="test_module",
            title="test_operation",
            business_type="test_business",
            method="test_method",
            request_method="GET",
            operator_type="test_operator",
            oper_name="test_operator_name",
            dept_name="test_dept",
            oper_url="/test/url",
            oper_ip="192.168.1.1",
            oper_location="test_location",
            oper_param="test_param",
            json_result="test_result",
            status=True,
            error_msg="test_error",
            cost_time=100,
            user=self.user
        )
        operation_log.save()
        
        self.assertEqual(operation_log.id, operation_log_id)
        self.assertEqual(operation_log.module, "test_module")
        self.assertEqual(operation_log.title, "test_operation")
        self.assertEqual(operation_log.business_type, "test_business")
        self.assertEqual(operation_log.method, "test_method")
        self.assertEqual(operation_log.request_method, "GET")
        self.assertEqual(operation_log.operator_type, "test_operator")
        self.assertEqual(operation_log.oper_name, "test_operator_name")
        self.assertEqual(operation_log.dept_name, "test_dept")
        self.assertEqual(operation_log.oper_url, "/test/url")
        self.assertEqual(operation_log.oper_ip, "192.168.1.1")
        self.assertEqual(operation_log.oper_location, "test_location")
        self.assertEqual(operation_log.oper_param, "test_param")
        self.assertEqual(operation_log.json_result, "test_result")
        self.assertEqual(operation_log.status, True)
        self.assertEqual(operation_log.error_msg, "test_error")
        self.assertEqual(operation_log.cost_time, 100)
        self.assertEqual(operation_log.user, self.user)
        
    def test_operation_log_str_representation(self):
        """测试操作日志字符串表示"""
        operation_log = OperationLog(
            id=uuid.uuid4().hex[:32],
            module="test_module",
            title="test_operation",
            business_type="test_business",
            method="test_method",
            request_method="GET",
            operator_type="test_operator",
            oper_name="test_operator_name",
            dept_name="test_dept",
            oper_url="/test/url",
            oper_ip="192.168.1.1",
            oper_location="test_location",
            oper_param="test_param",
            json_result="test_result",
            status=True,
            cost_time=100,
            user=self.user
        )
        operation_log.save()
        
        expected_str = f"OperationLog {operation_log.title} by {operation_log.oper_name}"
        self.assertEqual(str(operation_log), expected_str)
        
    def test_operation_log_optional_fields(self):
        """测试操作日志可选字段"""
        operation_log = OperationLog(
            id=uuid.uuid4().hex[:32],
            module="test_module",
            title="test_operation",
            business_type="test_business",
            method="test_method",
            request_method="GET",
            operator_type="test_operator",
            oper_name="test_operator_name",
            dept_name="test_dept",
            oper_url="/test/url",
            oper_ip="192.168.1.1",
            oper_location="test_location",
            oper_param="test_param",
            json_result="test_result",
            status=True,
            cost_time=100,
            user=self.user
            # 不设置error_msg
        )
        operation_log.save()
        
        self.assertIsNone(operation_log.error_msg)