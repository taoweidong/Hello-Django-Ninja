"""
测试权限仓储实现
"""

from django.test import TestCase
from django.contrib.auth.models import Permission
from app.infrastructure.persistence.repos.permission_repo_impl import DjangoORMPermissionRepository
from unittest.mock import patch, MagicMock


class TestDjangoORMPermissionRepository(TestCase):
    def setUp(self):
        """测试初始化"""
        self.repository = DjangoORMPermissionRepository()
        
    def test_permission_repository_save(self):
        """测试权限仓储保存权限"""
        # 创建测试权限
        permission = Permission(name="test_permission", codename="test_codename")
        
        # 使用mock避免实际数据库操作
        with patch.object(permission, 'save') as mock_save:
            self.repository.save(permission)
            mock_save.assert_called_once()
            
    def test_permission_repository_find_by_id(self):
        """测试权限仓储根据ID查找权限"""
        permission_id = 1
        mock_permission = MagicMock()
        
        with patch('app.infrastructure.persistence.repos.permission_repo_impl.Permission.objects.get', return_value=mock_permission) as mock_get:
            result = self.repository.find_by_id(permission_id)
            mock_get.assert_called_once_with(pk=permission_id)
            self.assertEqual(result, mock_permission)
            
    def test_permission_repository_find_by_id_not_found(self):
        """测试权限仓储根据ID查找权限（未找到）"""
        permission_id = 1
        
        with patch('app.infrastructure.persistence.repos.permission_repo_impl.Permission.objects.get') as mock_get:
            from django.core.exceptions import ObjectDoesNotExist
            mock_get.side_effect = ObjectDoesNotExist
            result = self.repository.find_by_id(permission_id)
            self.assertIsNone(result)
            
    def test_permission_repository_find_by_codename(self):
        """测试权限仓储根据代码名称查找权限"""
        codename = "test_codename"
        mock_permission = MagicMock()
        
        with patch('app.infrastructure.persistence.repos.permission_repo_impl.Permission.objects.get', return_value=mock_permission) as mock_get:
            result = self.repository.find_by_codename(codename)
            mock_get.assert_called_once_with(codename=codename)
            self.assertEqual(result, mock_permission)
            
    def test_permission_repository_find_by_codename_not_found(self):
        """测试权限仓储根据代码名称查找权限（未找到）"""
        codename = "test_codename"
        
        with patch('app.infrastructure.persistence.repos.permission_repo_impl.Permission.objects.get') as mock_get:
            from django.core.exceptions import ObjectDoesNotExist
            mock_get.side_effect = ObjectDoesNotExist
            result = self.repository.find_by_codename(codename)
            self.assertIsNone(result)
            
    def test_permission_repository_delete(self):
        """测试权限仓储删除权限"""
        permission_id = 1
        mock_permission = MagicMock()
        
        with patch('app.infrastructure.persistence.repos.permission_repo_impl.Permission.objects.get', return_value=mock_permission) as mock_get:
            with patch.object(mock_permission, 'delete') as mock_delete:
                result = self.repository.delete(permission_id)
                mock_get.assert_called_once_with(pk=permission_id)
                mock_delete.assert_called_once()
                self.assertTrue(result)
                
    def test_permission_repository_delete_not_found(self):
        """测试权限仓储删除权限（未找到）"""
        permission_id = 1
        
        with patch('app.infrastructure.persistence.repos.permission_repo_impl.Permission.objects.get') as mock_get:
            from django.core.exceptions import ObjectDoesNotExist
            mock_get.side_effect = ObjectDoesNotExist
            result = self.repository.delete(permission_id)
            self.assertFalse(result)
            
    def test_permission_repository_list_all(self):
        """测试权限仓储获取所有权限列表"""
        mock_permissions = [MagicMock(), MagicMock(), MagicMock()]
        
        with patch('app.infrastructure.persistence.repos.permission_repo_impl.Permission.objects.all', return_value=mock_permissions) as mock_all:
            result = self.repository.list_all()
            mock_all.assert_called_once()
            self.assertEqual(result, mock_permissions)