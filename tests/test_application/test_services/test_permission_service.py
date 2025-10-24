"""
测试权限应用服务
"""

from django.test import TestCase
from app.application.services.permission_service import PermissionService
from app.domain.repositories.permission_repository import PermissionRepository
from django.contrib.auth.models import Permission
from app.common.exception.exceptions import BusinessException
from unittest.mock import Mock


class TestPermissionService(TestCase):
    def setUp(self):
        """测试初始化"""
        # 创建mock的repository
        self.mock_repo = Mock(spec=PermissionRepository)
        self.permission_service = PermissionService(self.mock_repo)

    def test_create_permission_success(self):
        """测试成功创建权限"""
        # 准备测试数据
        permission_data = {
            "name": "测试权限",
            "codename": "test_permission",
            "content_type": "test_content_type"
        }
        
        # 创建mock的permission对象
        mock_permission = Mock(spec=Permission)
        mock_permission.pk = 1
        mock_permission.name = permission_data["name"]
        mock_permission.codename = permission_data["codename"]
        
        # 设置mock行为
        self.mock_repo.find_by_codename.return_value = None
        self.mock_repo.save.return_value = None
        
        result = self.permission_service.create_permission(**permission_data)
        
        # 验证结果
        self.assertEqual(result["name"], permission_data["name"])
        self.assertEqual(result["codename"], permission_data["codename"])
        self.mock_repo.save.assert_called_once()

    def test_create_permission_duplicate_codename(self):
        """测试创建权限时codename重复"""
        permission_data = {
            "name": "测试权限",
            "codename": "duplicate_codename",
            "content_type": "test_content_type"
        }
        
        # 设置mock行为，模拟codename已存在
        self.mock_repo.find_by_codename.return_value = Mock()
        
        with self.assertRaises(BusinessException) as context:
            self.permission_service.create_permission(**permission_data)
        
        self.assertIn("already exists", str(context.exception))
        self.mock_repo.save.assert_not_called()

    def test_get_permission_by_id_success(self):
        """测试成功获取权限"""
        permission_id = 1
        mock_permission = Mock(spec=Permission)
        mock_permission.pk = permission_id
        mock_permission.name = "测试权限"
        mock_permission.codename = "test_permission"
        
        # 设置mock行为
        self.mock_repo.find_by_id.return_value = mock_permission
        
        result = self.permission_service.get_permission_by_id(permission_id)
        
        self.assertEqual(result["id"], permission_id)
        self.assertEqual(result["name"], "测试权限")
        self.mock_repo.find_by_id.assert_called_once_with(permission_id)

    def test_get_permission_by_id_not_found(self):
        """测试获取不存在的权限"""
        permission_id = 999
        
        # 设置mock行为，模拟权限不存在
        self.mock_repo.find_by_id.return_value = None
        
        with self.assertRaises(BusinessException) as context:
            self.permission_service.get_permission_by_id(permission_id)
        
        self.assertIn("not found", str(context.exception))
        self.mock_repo.find_by_id.assert_called_once_with(permission_id)

    def test_update_permission_success(self):
        """测试成功更新权限"""
        permission_id = 1
        mock_permission = Mock(spec=Permission)
        mock_permission.pk = permission_id
        mock_permission.name = "原始权限"
        mock_permission.codename = "original_permission"
        
        update_data = {
            "name": "更新权限",
            "codename": "updated_permission",
            "content_type": "updated_content_type"
        }
        
        # 设置mock行为
        self.mock_repo.find_by_id.return_value = mock_permission
        self.mock_repo.save.return_value = None
        
        result = self.permission_service.update_permission(permission_id, **update_data)
        
        self.assertEqual(result["name"], update_data["name"])
        self.assertEqual(result["codename"], update_data["codename"])
        self.mock_repo.save.assert_called_once()

    def test_update_permission_not_found(self):
        """测试更新不存在的权限"""
        permission_id = 999
        
        # 设置mock行为，模拟权限不存在
        self.mock_repo.find_by_id.return_value = None
        
        with self.assertRaises(BusinessException) as context:
            self.permission_service.update_permission(permission_id, name="新权限")
        
        self.assertIn("not found", str(context.exception))
        self.mock_repo.find_by_id.assert_called_once_with(permission_id)
        self.mock_repo.save.assert_not_called()

    def test_delete_permission_success(self):
        """测试成功删除权限"""
        permission_id = 1
        
        # 设置mock行为
        self.mock_repo.delete.return_value = True
        
        result = self.permission_service.delete_permission(permission_id)
        
        self.assertTrue(result)
        self.mock_repo.delete.assert_called_once_with(permission_id)

    def test_delete_permission_not_found(self):
        """测试删除不存在的权限"""
        permission_id = 999
        
        # 设置mock行为，模拟删除失败（权限不存在）
        self.mock_repo.delete.return_value = False
        
        with self.assertRaises(BusinessException) as context:
            self.permission_service.delete_permission(permission_id)
        
        self.assertIn("not found", str(context.exception))
        self.mock_repo.delete.assert_called_once_with(permission_id)

    def test_list_permissions(self):
        """测试获取权限列表"""
        mock_permissions = []
        for i in range(3):
            mock_perm = Mock(spec=Permission)
            mock_perm.pk = i + 1
            mock_perm.name = f"权限{i}"
            mock_perm.codename = f"permission_{i}"
            mock_permissions.append(mock_perm)
        
        # 设置mock行为
        self.mock_repo.list_all.return_value = mock_permissions
        
        result = self.permission_service.list_permissions()
        
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0]["name"], "权限0")
        self.mock_repo.list_all.assert_called_once()