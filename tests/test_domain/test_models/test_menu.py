"""
测试菜单模型
"""

from django.test import TestCase
from app.domain.models.menu import Menu
from unittest.mock import patch, MagicMock
import uuid


class TestMenuModel(TestCase):
    def test_menu_creation(self):
        """测试菜单创建"""
        menu_id = uuid.uuid4().hex[:32]
        
        # 使用mock避免实际数据库操作
        with patch.object(Menu, 'save') as mock_save:
            menu = Menu(
                id=menu_id,
                name="test_menu",
                code="TEST_MENU",
                icon="test-icon",
                path="/test",
                component="TestComponent",
                redirect="/test/redirect",
                hidden=False,
                cache=True,
                sort=1,
                status=True,
                remark="Test menu remark",
                menu_type=1,
                rank=0,
                meta_id="meta123"
            )
            menu.save()
            
            mock_save.assert_called_once()
            
            self.assertEqual(menu.id, menu_id)
            self.assertEqual(menu.name, "test_menu")
            self.assertEqual(menu.code, "TEST_MENU")
            self.assertEqual(menu.icon, "test-icon")
            self.assertEqual(menu.path, "/test")
            self.assertEqual(menu.component, "TestComponent")
            self.assertEqual(menu.redirect, "/test/redirect")
            self.assertEqual(menu.hidden, False)
            self.assertEqual(menu.cache, True)
            self.assertEqual(menu.sort, 1)
            self.assertEqual(menu.status, True)
            self.assertEqual(menu.remark, "Test menu remark")
        
    def test_menu_str_representation(self):
        """测试菜单字符串表示"""
        # 使用mock避免实际数据库操作
        with patch.object(Menu, 'save') as mock_save:
            menu = Menu(
                id=uuid.uuid4().hex[:32],
                name="test_menu",
                code="TEST_MENU",
                menu_type=1,
                rank=0,
                meta_id="meta123"
            )
            menu.save()
            
            mock_save.assert_called_once()
            self.assertEqual(str(menu), "test_menu")
        
    def test_menu_with_parent(self):
        """测试菜单与父菜单关系"""
        # 使用mock避免实际数据库操作
        with patch.object(Menu, 'save') as mock_save:
            # 创建父菜单
            parent_menu = Menu(
                id=uuid.uuid4().hex[:32],
                name="parent_menu",
                code="PARENT_MENU",
                menu_type=1,
                rank=0,
                meta_id="meta123"
            )
            parent_menu.save()
            
            # 创建子菜单，使用parent_id而不是parent字段
            child_menu = Menu(
                id=uuid.uuid4().hex[:32],
                name="child_menu",
                code="CHILD_MENU",
                menu_type=1,
                rank=0,
                meta_id="meta123",
                parent_id=parent_menu.id
            )
            child_menu.save()
            
            # 验证父子关系通过parent_id
            self.assertEqual(child_menu.parent_id, parent_menu.id)
        
    def test_menu_optional_fields(self):
        """测试菜单可选字段"""
        # 使用mock避免实际数据库操作
        with patch.object(Menu, 'save') as mock_save:
            menu = Menu(
                id=uuid.uuid4().hex[:32],
                name="test_menu",
                code="TEST_MENU",
                menu_type=1,
                rank=0,
                meta_id="meta123"
                # 不设置可选字段
            )
            menu.save()
            
            mock_save.assert_called_once()
            self.assertIsNone(menu.icon)
            self.assertIsNone(menu.path)
            self.assertIsNone(menu.component)
            self.assertIsNone(menu.redirect)
            self.assertIsNone(menu.remark)