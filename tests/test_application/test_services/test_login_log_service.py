"""
测试登录日志应用服务
"""

from django.test import TestCase
from app.application.services.login_log_service import LoginLogService
from app.domain.models.login_log import LoginLog
from app.domain.models.user import User
from app.domain.repositories.login_log_repository import LoginLogRepository
from app.domain.repositories.user_repository import UserRepository
from app.common.exception.exceptions import BusinessException
from unittest.mock import Mock
import uuid


class TestLoginLogService(TestCase):
    def setUp(self):
        """测试初始化"""
        # 创建mock的repositories
        self.mock_login_log_repo = Mock(spec=LoginLogRepository)
        self.mock_user_repo = Mock(spec=UserRepository)
        self.login_log_service = LoginLogService(self.mock_login_log_repo, self.mock_user_repo)

    def test_create_login_log_success(self):
        """测试成功创建登录日志"""
        # 准备测试数据
        log_data = {
            "status": True,
            "login_type": 1,
            "ipaddress": "192.168.1.1",
            "browser": "Chrome",
            "system": "Windows",
            "agent": "Mozilla/5.0",
            "description": "登录成功",
            "creator": 1
        }
        
        # 创建mock的login_log对象
        mock_log = Mock(spec=LoginLog)
        mock_log.id = 1
        mock_log.status = log_data["status"]
        mock_log.login_type = log_data["login_type"]
        mock_log.ipaddress = log_data["ipaddress"]
        mock_log.browser = log_data["browser"]
        mock_log.system = log_data["system"]
        mock_log.agent = log_data["agent"]
        mock_log.creator = Mock(spec=User)
        mock_log.creator.id = log_data["creator"]
        mock_log.created_time = "2023-01-01T00:00:00Z"
        mock_log.updated_time = "2023-01-01T00:00:00Z"
        
        # 设置mock行为
        self.mock_login_log_repo.save.return_value = None
        
        # 执行测试
        result = self.login_log_service.create_login_log(**log_data)
        
        # 验证结果
        self.assertEqual(result["status"], log_data["status"])
        self.assertEqual(result["login_type"], log_data["login_type"])
        self.assertEqual(result["ipaddress"], log_data["ipaddress"])
        self.mock_login_log_repo.save.assert_called_once()

    def test_get_login_log_success(self):
        """测试成功获取登录日志"""
        log_id = 1
        mock_log = Mock(spec=LoginLog)
        mock_log.id = log_id
        mock_log.status = True
        mock_log.login_type = 1
        mock_log.ipaddress = "192.168.1.1"
        mock_log.browser = "Chrome"
        mock_log.system = "Windows"
        mock_log.agent = "Mozilla/5.0"
        mock_log.creator = Mock(spec=User)
        mock_log.creator.id = 1
        mock_log.created_time = "2023-01-01T00:00:00Z"
        mock_log.updated_time = "2023-01-01T00:00:00Z"
        
        # 设置mock行为
        self.mock_login_log_repo.find_by_id.return_value = mock_log
        
        result = self.login_log_service.get_login_log(log_id)
        
        self.assertEqual(result["id"], log_id)
        self.assertEqual(result["status"], True)
        self.mock_login_log_repo.find_by_id.assert_called_once_with(log_id)

    def test_get_login_log_not_found(self):
        """测试获取不存在的登录日志"""
        log_id = 999
        
        # 设置mock行为，模拟日志不存在
        self.mock_login_log_repo.find_by_id.return_value = None
        
        with self.assertRaises(BusinessException) as context:
            self.login_log_service.get_login_log(log_id)
        
        self.assertIn("not found", str(context.exception))
        self.mock_login_log_repo.find_by_id.assert_called_once_with(log_id)

    def test_update_login_log_success(self):
        """测试成功更新登录日志"""
        log_id = 1
        mock_log = Mock(spec=LoginLog)
        mock_log.id = log_id
        mock_log.status = True
        mock_log.login_type = 1
        mock_log.ipaddress = "192.168.1.1"
        mock_log.browser = "Chrome"
        mock_log.system = "Windows"
        mock_log.agent = "Mozilla/5.0"
        mock_log.creator = Mock(spec=User)
        mock_log.creator.id = 1
        mock_log.created_time = "2023-01-01T00:00:00Z"
        mock_log.updated_time = "2023-01-01T00:00:00Z"
        
        update_data = {
            "status": False,
            "login_type": 2,
            "ipaddress": "192.168.1.2",
            "browser": "Firefox",
            "system": "MacOS",
            "agent": "Mozilla/5.1"
        }
        
        # 设置mock行为
        self.mock_login_log_repo.find_by_id.return_value = mock_log
        self.mock_login_log_repo.save.return_value = None
        
        result = self.login_log_service.update_login_log(log_id, **update_data)
        
        self.assertEqual(result["status"], update_data["status"])
        self.assertEqual(result["login_type"], update_data["login_type"])
        self.assertEqual(result["ipaddress"], update_data["ipaddress"])
        self.mock_login_log_repo.save.assert_called_once()

    def test_update_login_log_not_found(self):
        """测试更新不存在的登录日志"""
        log_id = 999
        
        # 设置mock行为，模拟日志不存在
        self.mock_login_log_repo.find_by_id.return_value = None
        
        with self.assertRaises(BusinessException) as context:
            self.login_log_service.update_login_log(log_id, status=False)
        
        self.assertIn("not found", str(context.exception))
        self.mock_login_log_repo.find_by_id.assert_called_once_with(log_id)
        self.mock_login_log_repo.save.assert_not_called()

    def test_delete_login_log_success(self):
        """测试成功删除登录日志"""
        log_id = 1
        
        # 设置mock行为
        self.mock_login_log_repo.delete.return_value = True
        
        result = self.login_log_service.delete_login_log(log_id)
        
        self.assertTrue(result)
        self.mock_login_log_repo.delete.assert_called_once_with(log_id)

    def test_delete_login_log_not_found(self):
        """测试删除不存在的登录日志"""
        log_id = 999
        
        # 设置mock行为，模拟删除失败（日志不存在）
        self.mock_login_log_repo.delete.return_value = False
        
        with self.assertRaises(BusinessException) as context:
            self.login_log_service.delete_login_log(log_id)
        
        self.assertIn("not found", str(context.exception))
        self.mock_login_log_repo.delete.assert_called_once_with(log_id)

    def test_list_login_logs(self):
        """测试获取登录日志列表"""
        mock_logs = []
        for i in range(3):
            mock_log = Mock(spec=LoginLog)
            mock_log.id = i + 1
            mock_log.status = i % 2 == 0
            mock_log.login_type = i + 1
            mock_log.ipaddress = f"192.168.1.{i+1}"
            mock_log.browser = f"Browser{i}"
            mock_log.system = f"System{i}"
            mock_log.agent = f"Agent{i}"
            mock_log.creator = Mock(spec=User)
            mock_log.creator.id = i + 1
            mock_log.created_time = "2023-01-01T00:00:00Z"
            mock_log.updated_time = "2023-01-01T00:00:00Z"
            mock_logs.append(mock_log)
        
        # 设置mock行为
        self.mock_login_log_repo.list_all.return_value = mock_logs
        
        result = self.login_log_service.list_login_logs()
        
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0]["id"], 1)
        self.mock_login_log_repo.list_all.assert_called_once()