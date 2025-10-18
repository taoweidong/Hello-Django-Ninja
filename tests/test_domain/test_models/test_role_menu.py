"""
测试角色菜单关联模型
"""

from django.test import TestCase
from app.domain.models.role_menu import RoleMenu
from app.domain.models.role import Role
from app.domain.models.menu import Menu
from unittest.mock import patch
import uuid


class TestRoleMenuModel(TestCase):
    def setUp(self):
        """测试初始化"""
        # 使用mock避免实际数据库操作
        with patch.object(Role, 'save') as mock_role_save:
            with patch.object(Menu, 'save') as mock_menu_save:
                # 创建测试角色
                self.role = Role(
                    id=uuid.uuid4().hex[:32],
                    name="test_role",
                    code="TEST_ROLE"
                )
                self.role.save()
                
                # 创建测试菜单
                self.menu = Menu(
                    id=uuid.uuid4().hex[:32],
                    name="test_menu",
                    code="TEST_MENU"
                )
                self.menu.save()
        
    def test_role_menu_creation(self):
        """测试角色菜单关联创建"""
        role_menu_id = uuid.uuid4().hex[:32]
        
        # 使用mock避免实际数据库操作
        with patch.object(RoleMenu, 'save') as mock_save:
            role_menu = RoleMenu(
                id=role_menu_id,
                role=self.role,
                menu=self.menu
            )
            role_menu.save()
            
            mock_save.assert_called_once()
            
            self.assertEqual(role_menu.id, role_menu_id)
            self.assertEqual(role_menu.role, self.role)
            self.assertEqual(role_menu.menu, self.menu)
        
    def test_role_menu_str_representation(self):
        """测试角色菜单关联字符串表示"""
        # 使用mock避免实际数据库操作
        with patch.object(RoleMenu, 'save') as mock_save:
            role_menu = RoleMenu(
                id=uuid.uuid4().hex[:32],
                role=self.role,
                menu=self.menu
            )
            role_menu.save()
            
            mock_save.assert_called_once()
            
            expected_str = f"RoleMenu for role {self.role} and menu {self.menu}"
            self.assertEqual(str(role_menu), expected_str)