"""
测试操作日志应用服务
"""

from django.test import TestCase
from app.application.services.operation_log_service import OperationLogService
from app.domain.models.operation_log import OperationLog
from app.domain.models.user import User
from app.common.exception.exceptions import BusinessException
from unittest.mock import Mock, patch
import uuid


class TestOperationLogService(TestCase):
    def setUp(self):
        """测试初始化"""
        self.operation_log_service = OperationLogService()

    def test_create_operation_log_success(self):
        """测试成功创建操作日志"""
        # 准备测试数据
        log_data = {
            "module": "测试模块",
            "path": "/test",
            "body": "测试内容",
            "method": "GET",
            "ipaddress": "192.168.1.1",
            "browser": "Chrome",
            "system": "Windows",
            "response_code": 200,
            "response_result": "成功",
            "status_code": 200,
            "description": "测试日志",
            "creator_id": 1
        }
        
        # 创建mock的user对象
        mock_user = Mock(spec=User)
        mock_user.id = log_data["creator_id"]
        
        # 创建mock的operation_log对象
        mock_log = Mock(spec=OperationLog)
        mock_log.id = 1
        mock_log.module = log_data["module"]
        mock_log.path = log_data["path"]
        mock_log.body = log_data["body"]
        mock_log.method = log_data["method"]
        mock_log.ipaddress = log_data["ipaddress"]
        mock_log.browser = log_data["browser"]
        mock_log.system = log_data["system"]
        mock_log.response_code = log_data["response_code"]
        mock_log.response_result = log_data["response_result"]
        mock_log.status_code = log_data["status_code"]
        mock_log.description = log_data["description"]
        mock_log.creator = mock_user
        mock_log.created_time = "2023-01-01T00:00:00Z"
        mock_log.updated_time = "2023-01-01T00:00:00Z"
        
        # 设置mock行为
        with patch('app.application.services.operation_log_service.User') as mock_user_class:
            with patch('app.application.services.operation_log_service.OperationLog') as mock_log_class:
                # 模拟creator存在
                mock_user_class.objects.get.return_value = mock_user
                mock_log_class.return_value = mock_log
                mock_log.save.return_value = None
                
                result = self.operation_log_service.create_operation_log(**log_data)
                
                # 验证结果
                self.assertEqual(result["module"], log_data["module"])
                self.assertEqual(result["path"], log_data["path"])
                self.assertEqual(result["method"], log_data["method"])

    def test_create_operation_log_user_not_found(self):
        """测试创建操作日志时用户不存在"""
        log_data = {
            "module": "测试模块",
            "path": "/test",
            "body": "测试内容",
            "method": "GET",
            "ipaddress": "192.168.1.1",
            "browser": "Chrome",
            "system": "Windows",
            "response_code": 200,
            "response_result": "成功",
            "status_code": 200,
            "description": "测试日志",
            "creator_id": 999
        }
        
        # 设置mock行为，模拟用户不存在
        with patch('app.application.services.operation_log_service.User') as mock_user_class:
            mock_user_class.objects.get.side_effect = User.DoesNotExist
            
            with self.assertRaises(BusinessException) as context:
                self.operation_log_service.create_operation_log(**log_data)
            
            self.assertIn("not found", str(context.exception))

    def test_get_operation_log_success(self):
        """测试成功获取操作日志"""
        log_id = 1
        mock_user = Mock(spec=User)
        mock_user.id = 1
        
        mock_log = Mock(spec=OperationLog)
        mock_log.id = log_id
        mock_log.module = "测试模块"
        mock_log.path = "/test"
        mock_log.body = "测试内容"
        mock_log.method = "GET"
        mock_log.ipaddress = "192.168.1.1"
        mock_log.browser = "Chrome"
        mock_log.system = "Windows"
        mock_log.response_code = 200
        mock_log.response_result = "成功"
        mock_log.status_code = 200
        mock_log.description = "测试日志"
        mock_log.creator = mock_user
        mock_log.created_time = "2023-01-01T00:00:00Z"
        mock_log.updated_time = "2023-01-01T00:00:00Z"
        
        # 设置mock行为
        with patch('app.application.services.operation_log_service.OperationLog.objects.get') as mock_get:
            mock_get.return_value = mock_log
            
            result = self.operation_log_service.get_operation_log(log_id)
            
            self.assertEqual(result["id"], log_id)
            self.assertEqual(result["module"], "测试模块")
            mock_get.assert_called_once_with(id=log_id)

    def test_get_operation_log_not_found(self):
        """测试获取不存在的操作日志"""
        log_id = 999
        
        # 设置mock行为，模拟日志不存在
        with patch('app.application.services.operation_log_service.OperationLog.objects.get') as mock_get:
            mock_get.side_effect = OperationLog.DoesNotExist
            
            with self.assertRaises(BusinessException) as context:
                self.operation_log_service.get_operation_log(log_id)
            
            self.assertIn("not found", str(context.exception))

    def test_update_operation_log_success(self):
        """测试成功更新操作日志"""
        log_id = 1
        mock_user = Mock(spec=User)
        mock_user.id = 1
        
        mock_log = Mock(spec=OperationLog)
        mock_log.id = log_id
        mock_log.module = "原始模块"
        mock_log.path = "/original"
        mock_log.body = "原始内容"
        mock_log.method = "GET"
        mock_log.ipaddress = "192.168.1.1"
        mock_log.browser = "Chrome"
        mock_log.system = "Windows"
        mock_log.response_code = 200
        mock_log.response_result = "成功"
        mock_log.status_code = 200
        mock_log.description = "原始日志"
        mock_log.creator = mock_user
        mock_log.created_time = "2023-01-01T00:00:00Z"
        mock_log.updated_time = "2023-01-01T00:00:00Z"
        mock_log.save.return_value = None
        
        update_data = {
            "module": "更新模块",
            "path": "/updated",
            "body": "更新内容",
            "method": "POST",
            "ipaddress": "192.168.1.2",
            "browser": "Firefox",
            "system": "MacOS",
            "response_code": 404,
            "response_result": "失败",
            "status_code": 404,
            "description": "更新日志"
        }
        
        # 设置mock行为
        with patch('app.application.services.operation_log_service.OperationLog.objects.get') as mock_get:
            mock_get.return_value = mock_log
            
            result = self.operation_log_service.update_operation_log(log_id, **update_data)
            
            self.assertEqual(result["module"], update_data["module"])
            self.assertEqual(result["path"], update_data["path"])
            self.assertEqual(result["method"], update_data["method"])

    def test_update_operation_log_not_found(self):
        """测试更新不存在的操作日志"""
        log_id = 999
        
        # 设置mock行为，模拟日志不存在
        with patch('app.application.services.operation_log_service.OperationLog.objects.get') as mock_get:
            mock_get.side_effect = OperationLog.DoesNotExist
            
            with self.assertRaises(BusinessException) as context:
                self.operation_log_service.update_operation_log(log_id, module="新模块")
            
            self.assertIn("not found", str(context.exception))

    def test_delete_operation_log_success(self):
        """测试成功删除操作日志"""
        log_id = 1
        mock_log = Mock(spec=OperationLog)
        mock_log.delete.return_value = None
        
        # 设置mock行为
        with patch('app.application.services.operation_log_service.OperationLog.objects.get') as mock_get:
            mock_get.return_value = mock_log
            
            result = self.operation_log_service.delete_operation_log(log_id)
            
            self.assertTrue(result)
            mock_log.delete.assert_called_once()

    def test_delete_operation_log_not_found(self):
        """测试删除不存在的操作日志"""
        log_id = 999
        
        # 设置mock行为，模拟日志不存在
        with patch('app.application.services.operation_log_service.OperationLog.objects.get') as mock_get:
            mock_get.side_effect = OperationLog.DoesNotExist
            
            with self.assertRaises(BusinessException) as context:
                self.operation_log_service.delete_operation_log(log_id)
            
            self.assertIn("not found", str(context.exception))

    def test_list_operation_logs(self):
        """测试获取操作日志列表"""
        mock_logs = []
        for i in range(3):
            mock_user = Mock(spec=User)
            mock_user.id = i + 1
            
            mock_log = Mock(spec=OperationLog)
            mock_log.id = i + 1
            mock_log.module = f"模块{i}"
            mock_log.path = f"/path{i}"
            mock_log.body = f"内容{i}"
            mock_log.method = "GET" if i % 2 == 0 else "POST"
            mock_log.ipaddress = f"192.168.1.{i+1}"
            mock_log.browser = f"浏览器{i}"
            mock_log.system = f"系统{i}"
            mock_log.response_code = 200 + i
            mock_log.response_result = "成功" if i % 2 == 0 else "失败"
            mock_log.status_code = 200 + i
            mock_log.description = f"日志{i}"
            mock_log.creator = mock_user
            mock_log.created_time = "2023-01-01T00:00:00Z"
            mock_log.updated_time = "2023-01-01T00:00:00Z"
            mock_logs.append(mock_log)
        
        # 设置mock行为
        with patch('app.application.services.operation_log_service.OperationLog.objects.all') as mock_all:
            mock_all.return_value = mock_logs
            
            result = self.operation_log_service.list_operation_logs()
            
            self.assertEqual(len(result), 3)
            self.assertEqual(result[0]["module"], "模块0")