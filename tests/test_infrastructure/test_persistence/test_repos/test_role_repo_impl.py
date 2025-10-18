"""
测试角色仓储实现
"""

from django.test import TestCase
from app.infrastructure.persistence.repos.role_repo_impl import DjangoORMRoleRepository
from app.domain.models.role import Role
from unittest.mock import patch, MagicMock
import uuid


class TestDjangoORMRoleRepository(TestCase):
    def setUp(self):
        """测试初始化"""
        self.repository = DjangoORMRoleRepository()
        
    def test_role_repository_initialization(self):
        """测试角色仓储初始化"""
        self.assertIsNotNone(self.repository.RoleModel)
        
    def test_role_repository_save(self):
        """测试角色仓储保存角色"""
        # 创建测试角色
        role = Role(name="test_role", description="Test role")
        
        # 使用mock避免实际数据库操作
        with patch.object(role, 'save') as mock_save:
            self.repository.save(role)
            mock_save.assert_called_once()
            
    def test_role_repository_find_by_id(self):
        """测试角色仓储根据ID查找角色"""
        role_id = "test_role_id"
        mock_role = MagicMock()
        
        with patch('app.infrastructure.persistence.repos.role_repo_impl.Role.objects.get', return_value=mock_role) as mock_get:
            result = self.repository.find_by_id(role_id)
            mock_get.assert_called_once_with(pk=role_id)
            self.assertEqual(result, mock_role)
            
    def test_role_repository_find_by_id_with_int_id(self):
        """测试角色仓储根据整数ID查找角色"""
        role_id = 1
        mock_role = MagicMock()
        
        with patch('app.infrastructure.persistence.repos.role_repo_impl.Role.objects.get', return_value=mock_role) as mock_get:
            result = self.repository.find_by_id(role_id)
            mock_get.assert_called_once_with(pk=str(role_id))
            self.assertEqual(result, mock_role)
            
    def test_role_repository_find_by_id_not_found(self):
        """测试角色仓储根据ID查找角色（未找到）"""
        role_id = "test_role_id"
        
        with patch('app.infrastructure.persistence.repos.role_repo_impl.Role.objects.get') as mock_get:
            from django.core.exceptions import ObjectDoesNotExist
            mock_get.side_effect = ObjectDoesNotExist
            result = self.repository.find_by_id(role_id)
            self.assertIsNone(result)
            
    def test_role_repository_find_by_name(self):
        """测试角色仓储根据名称查找角色"""
        name = "test_role"
        mock_role = MagicMock()
        
        with patch('app.infrastructure.persistence.repos.role_repo_impl.Role.objects.get', return_value=mock_role) as mock_get:
            result = self.repository.find_by_name(name)
            mock_get.assert_called_once_with(name=name)
            self.assertEqual(result, mock_role)
            
    def test_role_repository_find_by_name_not_found(self):
        """测试角色仓储根据名称查找角色（未找到）"""
        name = "test_role"
        
        with patch('app.infrastructure.persistence.repos.role_repo_impl.Role.objects.get') as mock_get:
            from django.core.exceptions import ObjectDoesNotExist
            mock_get.side_effect = ObjectDoesNotExist
            result = self.repository.find_by_name(name)
            self.assertIsNone(result)
            
    def test_role_repository_delete(self):
        """测试角色仓储删除角色"""
        role_id = "test_role_id"
        mock_role = MagicMock()
        
        with patch('app.infrastructure.persistence.repos.role_repo_impl.Role.objects.get', return_value=mock_role) as mock_get:
            with patch.object(mock_role, 'delete') as mock_delete:
                result = self.repository.delete(role_id)
                mock_get.assert_called_once_with(pk=role_id)
                mock_delete.assert_called_once()
                self.assertTrue(result)
                
    def test_role_repository_delete_with_int_id(self):
        """测试角色仓储删除角色（使用整数ID）"""
        role_id = 1
        mock_role = MagicMock()
        
        with patch('app.infrastructure.persistence.repos.role_repo_impl.Role.objects.get', return_value=mock_role) as mock_get:
            with patch.object(mock_role, 'delete') as mock_delete:
                result = self.repository.delete(role_id)
                mock_get.assert_called_once_with(pk=str(role_id))
                mock_delete.assert_called_once()
                self.assertTrue(result)
                
    def test_role_repository_delete_not_found(self):
        """测试角色仓储删除角色（未找到）"""
        role_id = "test_role_id"
        
        with patch('app.infrastructure.persistence.repos.role_repo_impl.Role.objects.get') as mock_get:
            from django.core.exceptions import ObjectDoesNotExist
            mock_get.side_effect = ObjectDoesNotExist
            result = self.repository.delete(role_id)
            self.assertFalse(result)
            
    def test_role_repository_list_all(self):
        """测试角色仓储获取所有角色列表"""
        mock_roles = [MagicMock(), MagicMock(), MagicMock()]
        
        with patch('app.infrastructure.persistence.repos.role_repo_impl.Role.objects.all', return_value=mock_roles) as mock_all:
            result = self.repository.list_all()
            mock_all.assert_called_once()
            self.assertEqual(result, mock_roles)
            
    def test_role_repository_assign_permissions(self):
        """测试角色仓储分配权限"""
        role_id = "test_role_id"
        permission_ids = [1, 2, 3]
        mock_role = MagicMock()
        
        with patch('app.infrastructure.persistence.repos.role_repo_impl.Role.objects.get', return_value=mock_role) as mock_get:
            self.repository.assign_permissions(role_id, permission_ids)
            mock_get.assert_called_once_with(pk=role_id)
            mock_role.permissions.set.assert_called_once_with(permission_ids)
            
    def test_role_repository_assign_permissions_not_found(self):
        """测试角色仓储分配权限（角色未找到）"""
        role_id = "test_role_id"
        permission_ids = [1, 2, 3]
        
        with patch('app.infrastructure.persistence.repos.role_repo_impl.Role.objects.get') as mock_get:
            from django.core.exceptions import ObjectDoesNotExist
            mock_get.side_effect = ObjectDoesNotExist
            # 不应该抛出异常
            try:
                self.repository.assign_permissions(role_id, permission_ids)
            except Exception as e:
                self.fail(f"Expected no exception, but got {type(e).__name__}: {e}")