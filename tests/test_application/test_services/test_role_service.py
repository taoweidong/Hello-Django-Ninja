"""
测试角色应用服务
"""

from django.test import TestCase
from app.application.services.role_service import RoleService
from app.domain.repositories.role_repository import RoleRepository
from app.domain.models.role import Role
from app.common.exception.exceptions import BusinessException
from unittest.mock import Mock
import uuid


class TestRoleService(TestCase):
    def setUp(self):
        """测试初始化"""
        # 创建mock的repository
        self.mock_repo = Mock(spec=RoleRepository)
        self.role_service = RoleService(self.mock_repo)

    def test_create_role_success(self):
        """测试成功创建角色"""
        # 准备测试数据
        role_data = {
            "name": "测试角色",
            "description": "测试角色描述"
        }
        
        # 创建mock的role对象
        mock_role = Mock(spec=Role)
        mock_role.id = str(uuid.uuid4())
        mock_role.name = role_data["name"]
        mock_role.description = role_data["description"]
        
        # 设置mock行为
        self.mock_repo.find_by_name.return_value = None
        self.mock_repo.save.return_value = None
        
        result = self.role_service.create_role(**role_data)
        
        # 验证结果
        self.assertEqual(result["name"], role_data["name"])
        self.assertEqual(result["description"], role_data["description"])
        self.mock_repo.save.assert_called_once()

    def test_create_role_duplicate_name(self):
        """测试创建角色时name重复"""
        role_data = {
            "name": "重复角色",
            "description": "测试角色描述"
        }
        
        # 设置mock行为，模拟name已存在
        self.mock_repo.find_by_name.return_value = Mock()
        
        with self.assertRaises(BusinessException) as context:
            self.role_service.create_role(**role_data)
        
        self.assertIn("already exists", str(context.exception))
        self.mock_repo.save.assert_not_called()

    def test_get_role_success(self):
        """测试成功获取角色"""
        role_id = str(uuid.uuid4())
        mock_role = Mock(spec=Role)
        mock_role.id = role_id
        mock_role.name = "测试角色"
        mock_role.description = "测试角色描述"
        
        # 设置mock行为
        self.mock_repo.find_by_id.return_value = mock_role
        
        result = self.role_service.get_role(role_id)
        
        self.assertEqual(result["id"], role_id)
        self.assertEqual(result["name"], "测试角色")
        self.mock_repo.find_by_id.assert_called_once_with(role_id)

    def test_get_role_by_int_id(self):
        """测试使用整数ID获取角色"""
        role_id = 1
        role_uuid = "1"  # 修改为字符串形式以匹配服务中的转换
        mock_role = Mock(spec=Role)
        mock_role.id = role_uuid
        mock_role.name = "测试角色"
        mock_role.description = "测试角色描述"
        
        # 设置mock行为
        self.mock_repo.find_by_id.return_value = mock_role
        
        result = self.role_service.get_role(role_id)
        
        self.assertEqual(result["id"], role_uuid)
        self.mock_repo.find_by_id.assert_called_once_with(role_uuid)

    def test_get_role_not_found(self):
        """测试获取不存在的角色"""
        role_id = str(uuid.uuid4())
        
        # 设置mock行为，模拟角色不存在
        self.mock_repo.find_by_id.return_value = None
        
        with self.assertRaises(BusinessException) as context:
            self.role_service.get_role(role_id)
        
        self.assertIn("not found", str(context.exception))
        self.mock_repo.find_by_id.assert_called_once_with(role_id)

    def test_update_role_success(self):
        """测试成功更新角色"""
        role_id = str(uuid.uuid4())
        mock_role = Mock(spec=Role)
        mock_role.id = role_id
        mock_role.name = "原始角色"
        mock_role.description = "原始角色描述"
        
        update_data = {
            "name": "更新角色",
            "description": "更新角色描述"
        }
        
        # 设置mock行为
        self.mock_repo.find_by_id.return_value = mock_role
        self.mock_repo.save.return_value = None
        
        result = self.role_service.update_role(role_id, **update_data)
        
        self.assertEqual(result["name"], update_data["name"])
        self.assertEqual(result["description"], update_data["description"])
        self.mock_repo.save.assert_called_once()

    def test_update_role_by_int_id(self):
        """测试使用整数ID更新角色"""
        role_id = 1
        role_uuid = "1"  # 修改为字符串形式以匹配服务中的转换
        mock_role = Mock(spec=Role)
        mock_role.id = role_uuid
        mock_role.name = "原始角色"
        mock_role.description = "原始角色描述"
        
        update_data = {
            "name": "更新角色",
            "description": "更新角色描述"
        }
        
        # 设置mock行为
        self.mock_repo.find_by_id.return_value = mock_role
        self.mock_repo.save.return_value = None
        
        result = self.role_service.update_role(role_id, **update_data)
        
        self.assertEqual(result["name"], update_data["name"])
        self.assertEqual(result["description"], update_data["description"])
        self.mock_repo.save.assert_called_once()

    def test_update_role_not_found(self):
        """测试更新不存在的角色"""
        role_id = str(uuid.uuid4())
        
        # 设置mock行为，模拟角色不存在
        self.mock_repo.find_by_id.return_value = None
        
        with self.assertRaises(BusinessException) as context:
            self.role_service.update_role(role_id, name="新角色")
        
        self.assertIn("not found", str(context.exception))
        self.mock_repo.find_by_id.assert_called_once_with(role_id)
        self.mock_repo.save.assert_not_called()

    def test_delete_role_success(self):
        """测试成功删除角色"""
        role_id = str(uuid.uuid4())
        
        # 设置mock行为
        self.mock_repo.delete.return_value = True
        
        result = self.role_service.delete_role(role_id)
        
        self.assertTrue(result)
        self.mock_repo.delete.assert_called_once_with(role_id)

    def test_delete_role_by_int_id(self):
        """测试使用整数ID删除角色"""
        role_id = 1
        role_uuid = "1"  # 修改为字符串形式以匹配服务中的转换
        
        # 设置mock行为
        self.mock_repo.delete.return_value = True
        
        result = self.role_service.delete_role(role_id)
        
        self.assertTrue(result)
        self.mock_repo.delete.assert_called_once_with(role_uuid)

    def test_delete_role_not_found(self):
        """测试删除不存在的角色"""
        role_id = str(uuid.uuid4())
        
        # 设置mock行为，模拟删除失败（角色不存在）
        self.mock_repo.delete.return_value = False
        
        with self.assertRaises(BusinessException) as context:
            self.role_service.delete_role(role_id)
        
        self.assertIn("not found", str(context.exception))
        self.mock_repo.delete.assert_called_once_with(role_id)

    def test_list_roles(self):
        """测试获取角色列表"""
        mock_roles = []
        for i in range(3):
            mock_role = Mock(spec=Role)
            mock_role.id = str(uuid.uuid4())
            mock_role.name = f"角色{i}"
            mock_role.description = f"角色{i}描述"
            mock_roles.append(mock_role)
        
        # 设置mock行为
        self.mock_repo.list_all.return_value = mock_roles
        
        result = self.role_service.list_roles()
        
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0]["name"], "角色0")
        self.mock_repo.list_all.assert_called_once()

    def test_assign_permissions_to_role(self):
        """测试为角色分配权限"""
        role_id = str(uuid.uuid4())
        permission_ids = [1, 2, 3]
        
        # 设置mock行为
        self.mock_repo.assign_permissions.return_value = None
        
        # 执行测试
        self.role_service.assign_permissions_to_role(role_id, permission_ids)
        
        # 验证结果
        self.mock_repo.assign_permissions.assert_called_once_with(role_id, permission_ids)