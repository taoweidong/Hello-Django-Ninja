"""
测试用户应用服务
"""

from django.test import TestCase
from unittest.mock import Mock, patch
from app.application.services.user_service import UserService
from app.domain.repositories.user_repository import UserRepository
from app.domain.models.user import User
from app.common.exception.exceptions import BusinessException


class TestUserService(TestCase):
    def setUp(self):
        """测试初始化"""
        # 创建mock的repository
        self.mock_repo = Mock(spec=UserRepository)
        self.user_service = UserService(self.mock_repo)

    def test_create_user_success(self):
        """测试成功创建用户"""
        # 准备测试数据
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword"
        }
        
        # 创建mock的user对象
        mock_user = Mock(spec=User)
        mock_user.id = 1
        mock_user.username = user_data["username"]
        mock_user.email = user_data["email"]
        # 确保mock对象有set_password方法
        mock_user.set_password = Mock()
        
        # 设置mock行为
        self.mock_repo.find_by_username.return_value = None
        self.mock_repo.save.return_value = None
        
        # 修复：确保在create_user方法中创建的User对象能够正确调用set_password
        with patch('app.application.services.user_service.User') as mock_user_class:
            mock_user_class.return_value = mock_user
            result = self.user_service.create_user(**user_data)
        
        # 验证结果
        self.assertEqual(result["username"], user_data["username"])
        self.assertEqual(result["email"], user_data["email"])
        self.mock_repo.save.assert_called_once()
        mock_user.set_password.assert_called_once_with(user_data["password"])

    def test_create_user_duplicate_username(self):
        """测试创建用户时username重复"""
        user_data = {
            "username": "duplicateuser",
            "email": "test@example.com",
            "password": "testpassword"
        }
        
        # 设置mock行为，模拟username已存在
        self.mock_repo.find_by_username.return_value = Mock()
        
        with self.assertRaises(BusinessException) as context:
            self.user_service.create_user(**user_data)
        
        self.assertIn("already exists", str(context.exception))
        self.mock_repo.save.assert_not_called()

    def test_get_user_success(self):
        """测试成功获取用户"""
        user_id = 1
        mock_user = Mock(spec=User)
        mock_user.id = user_id
        mock_user.username = "testuser"
        mock_user.email = "test@example.com"
        
        # 设置mock行为
        self.mock_repo.find_by_id.return_value = mock_user
        
        result = self.user_service.get_user(user_id)
        
        self.assertEqual(result["id"], user_id)
        self.assertEqual(result["username"], "testuser")
        self.mock_repo.find_by_id.assert_called_once_with(user_id)

    def test_get_user_not_found(self):
        """测试获取不存在的用户"""
        user_id = 999
        
        # 设置mock行为，模拟用户不存在
        self.mock_repo.find_by_id.return_value = None
        
        with self.assertRaises(BusinessException) as context:
            self.user_service.get_user(user_id)
        
        self.assertIn("not found", str(context.exception))
        self.mock_repo.find_by_id.assert_called_once_with(user_id)

    def test_update_user_success(self):
        """测试成功更新用户"""
        user_id = 1
        mock_user = Mock(spec=User)
        mock_user.id = user_id
        mock_user.username = "originaluser"
        mock_user.email = "original@example.com"
        mock_user.set_password = Mock(return_value=None)  # 修复mock对象
        
        update_data = {
            "username": "updateduser",
            "email": "updated@example.com",
            "password": "newpassword"
        }
        
        # 设置mock行为
        self.mock_repo.find_by_id.return_value = mock_user
        self.mock_repo.save.return_value = None
        
        result = self.user_service.update_user(user_id, **update_data)
        
        self.assertEqual(result["username"], update_data["username"])
        self.assertEqual(result["email"], update_data["email"])
        self.mock_repo.save.assert_called_once()
        mock_user.set_password.assert_called_once_with(update_data["password"])

    def test_update_user_partial_fields(self):
        """测试部分更新用户信息"""
        user_id = 1
        mock_user = Mock(spec=User)
        mock_user.id = user_id
        mock_user.username = "originaluser"
        mock_user.email = "original@example.com"
        mock_user.set_password = Mock(return_value=None)  # 修复mock对象
        
        update_data = {
            "username": "updateduser"
        }
        
        # 设置mock行为
        self.mock_repo.find_by_id.return_value = mock_user
        self.mock_repo.save.return_value = None
        
        result = self.user_service.update_user(user_id, **update_data)
        
        self.assertEqual(result["username"], update_data["username"])
        self.mock_repo.save.assert_called_once()
        mock_user.set_password.assert_not_called()

    def test_update_user_not_found(self):
        """测试更新不存在的用户"""
        user_id = 999
        
        # 设置mock行为，模拟用户不存在
        self.mock_repo.find_by_id.return_value = None
        
        with self.assertRaises(BusinessException) as context:
            self.user_service.update_user(user_id, username="newuser")
        
        self.assertIn("not found", str(context.exception))
        self.mock_repo.find_by_id.assert_called_once_with(user_id)
        self.mock_repo.save.assert_not_called()

    def test_delete_user_success(self):
        """测试成功删除用户"""
        user_id = 1
        
        # 设置mock行为
        self.mock_repo.delete.return_value = True
        
        result = self.user_service.delete_user(user_id)
        
        self.assertTrue(result)
        self.mock_repo.delete.assert_called_once_with(user_id)

    def test_delete_user_not_found(self):
        """测试删除不存在的用户"""
        user_id = 999
        
        # 设置mock行为，模拟删除失败（用户不存在）
        self.mock_repo.delete.return_value = False
        
        with self.assertRaises(BusinessException) as context:
            self.user_service.delete_user(user_id)
        
        self.assertIn("not found", str(context.exception))
        self.mock_repo.delete.assert_called_once_with(user_id)

    def test_list_users(self):
        """测试获取用户列表"""
        mock_users = []
        for i in range(3):
            mock_user = Mock(spec=User)
            mock_user.id = i + 1
            mock_user.username = f"user{i}"
            mock_user.email = f"user{i}@example.com"
            mock_users.append(mock_user)
        
        # 设置mock行为
        self.mock_repo.list_all.return_value = mock_users
        
        result = self.user_service.list_users()
        
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0]["username"], "user0")
        self.mock_repo.list_all.assert_called_once()

    def test_assign_role_to_user(self):
        """测试为用户分配角色"""
        user_id = 1
        role_id = 1
        
        # 执行测试（当前实现为空，只测试方法可以被调用）
        self.user_service.assign_role_to_user(user_id, role_id)
        
        # 验证方法可以被调用（不会抛出异常）
        self.assertTrue(True)