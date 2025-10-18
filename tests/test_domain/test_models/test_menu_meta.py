"""
测试菜单元数据模型
"""

from django.test import TestCase
from app.domain.models.menu_meta import MenuMeta
from unittest.mock import patch
import uuid


class TestMenuMetaModel(TestCase):
    def test_menu_meta_creation(self):
        """测试菜单元数据创建"""
        menu_meta_id = uuid.uuid4().hex[:32]
        
        # 使用mock避免实际数据库操作
        with patch.object(MenuMeta, 'save') as mock_save:
            menu_meta = MenuMeta(
                id=menu_meta_id,
                title="test_menu_meta",
                icon="test-icon",
                hidden=False,
                cache=True,
                sort=1,
                status=True,
                remark="Test menu meta remark"
            )
            menu_meta.save()
            
            mock_save.assert_called_once()
            
            self.assertEqual(menu_meta.id, menu_meta_id)
            self.assertEqual(menu_meta.title, "test_menu_meta")
            self.assertEqual(menu_meta.icon, "test-icon")
            self.assertEqual(menu_meta.hidden, False)
            self.assertEqual(menu_meta.cache, True)
            self.assertEqual(menu_meta.sort, 1)
            self.assertEqual(menu_meta.status, True)
            self.assertEqual(menu_meta.remark, "Test menu meta remark")
        
    def test_menu_meta_str_representation(self):
        """测试菜单元数据字符串表示"""
        # 使用mock避免实际数据库操作
        with patch.object(MenuMeta, 'save') as mock_save:
            menu_meta = MenuMeta(
                id=uuid.uuid4().hex[:32],
                title="test_menu_meta"
            )
            menu_meta.save()
            
            mock_save.assert_called_once()
            self.assertEqual(str(menu_meta), "test_menu_meta")
        
    def test_menu_meta_optional_fields(self):
        """测试菜单元数据可选字段"""
        # 使用mock避免实际数据库操作
        with patch.object(MenuMeta, 'save') as mock_save:
            menu_meta = MenuMeta(
                id=uuid.uuid4().hex[:32],
                title="test_menu_meta"
                # 不设置可选字段
            )
            menu_meta.save()
            
            mock_save.assert_called_once()
            self.assertIsNone(menu_meta.icon)
            self.assertIsNone(menu_meta.remark)