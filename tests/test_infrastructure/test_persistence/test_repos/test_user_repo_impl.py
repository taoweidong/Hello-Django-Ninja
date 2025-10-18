"""
测试用户仓储实现
"""

from django.test import TestCase
from app.infrastructure.persistence.repos.user_repo_impl import DjangoORMUserRepository
from app.domain.models.user import User
from unittest.mock import patch, MagicMock
import uuid


class TestDjangoORMUserRepository(TestCase):
    def setUp(self):
        """测试初始化"""
        self.repository = DjangoORMUserRepository()
        
    def test_user_repository_initialization(self):
        """测试用户仓储初始化"""
        self.assertIsNotNone(self.repository.UserModel)
        
    def test_user_repository_save(self):
        """测试用户仓储保存用户"""
        # 创建测试用户
        user = User(username="testuser", email="test@example.com")
        user.set_password("testpass123")
        
        # 使用mock避免实际数据库操作
        with patch.object(user, 'save') as mock_save:
            self.repository.save(user)
            mock_save.assert_called_once()
            
    def test_user_repository_find_by_id(self):
        """测试用户仓储根据ID查找用户"""
        user_id = 1
        mock_user = MagicMock()
        
        with patch('app.infrastructure.persistence.repos.user_repo_impl.User.objects.get', return_value=mock_user) as mock_get:
            result = self.repository.find_by_id(user_id)
            mock_get.assert_called_once_with(pk=user_id)
            self.assertEqual(result, mock_user)
            
    def test_user_repository_find_by_id_not_found(self):
        """测试用户仓储根据ID查找用户（未找到）"""
        user_id = 1
        
        with patch('app.infrastructure.persistence.repos.user_repo_impl.User.objects.get') as mock_get:
            from django.core.exceptions import ObjectDoesNotExist
            mock_get.side_effect = ObjectDoesNotExist
            result = self.repository.find_by_id(user_id)
            self.assertIsNone(result)
            
    def test_user_repository_find_by_username(self):
        """测试用户仓储根据用户名查找用户"""
        username = "testuser"
        mock_user = MagicMock()
        
        with patch('app.infrastructure.persistence.repos.user_repo_impl.User.objects.get', return_value=mock_user) as mock_get:
            result = self.repository.find_by_username(username)
            mock_get.assert_called_once_with(username=username)
            self.assertEqual(result, mock_user)
            
    def test_user_repository_find_by_username_not_found(self):
        """测试用户仓储根据用户名查找用户（未找到）"""
        username = "testuser"
        
        with patch('app.infrastructure.persistence.repos.user_repo_impl.User.objects.get') as mock_get:
            from django.core.exceptions import ObjectDoesNotExist
            mock_get.side_effect = ObjectDoesNotExist
            result = self.repository.find_by_username(username)
            self.assertIsNone(result)
            
    def test_user_repository_delete(self):
        """测试用户仓储删除用户"""
        user_id = 1
        mock_user = MagicMock()
        
        with patch('app.infrastructure.persistence.repos.user_repo_impl.User.objects.get', return_value=mock_user) as mock_get:
            with patch.object(mock_user, 'delete') as mock_delete:
                result = self.repository.delete(user_id)
                mock_get.assert_called_once_with(pk=user_id)
                mock_delete.assert_called_once()
                self.assertTrue(result)
                
    def test_user_repository_delete_not_found(self):
        """测试用户仓储删除用户（未找到）"""
        user_id = 1
        
        with patch('app.infrastructure.persistence.repos.user_repo_impl.User.objects.get') as mock_get:
            from django.core.exceptions import ObjectDoesNotExist
            mock_get.side_effect = ObjectDoesNotExist
            result = self.repository.delete(user_id)
            self.assertFalse(result)
            
    def test_user_repository_list_all(self):
        """测试用户仓储获取所有用户列表"""
        mock_users = [MagicMock(), MagicMock(), MagicMock()]
        
        with patch('app.infrastructure.persistence.repos.user_repo_impl.User.objects.all', return_value=mock_users) as mock_all:
            result = self.repository.list_all()
            mock_all.assert_called_once()
            self.assertEqual(result, mock_users)