"""
测试菜单元数据应用服务
"""

from django.test import TestCase
from app.application.services.menu_meta_service import MenuMetaService
from app.domain.models.menu_meta import MenuMeta
from app.common.exception.exceptions import BusinessException
from unittest.mock import Mock, patch
import uuid


class TestMenuMetaService(TestCase):
    def setUp(self):
        """测试初始化"""
        self.menu_meta_service = MenuMetaService()

    def test_create_menu_meta_success(self):
        """测试成功创建菜单元数据"""
        # 准备测试数据
        meta_data = {
            "title": "测试菜单",
            "icon": "test-icon",
            "r_svg_name": "test-svg",
            "is_show_menu": True,
            "is_show_parent": True,
            "is_keepalive": True,
            "frame_url": "https://example.com",
            "frame_loading": False,
            "transition_enter": "slide-in",
            "transition_leave": "slide-out",
            "is_hidden_tag": False,
            "fixed_tag": True,
            "dynamic_level": 1
        }
        
        # 创建mock的menu_meta对象
        mock_meta = Mock(spec=MenuMeta)
        mock_meta.id = str(uuid.uuid4())
        mock_meta.title = meta_data["title"]
        mock_meta.icon = meta_data["icon"]
        mock_meta.r_svg_name = meta_data["r_svg_name"]
        mock_meta.is_show_menu = meta_data["is_show_menu"]
        mock_meta.is_show_parent = meta_data["is_show_parent"]
        mock_meta.is_keepalive = meta_data["is_keepalive"]
        mock_meta.frame_url = meta_data["frame_url"]
        mock_meta.frame_loading = meta_data["frame_loading"]
        mock_meta.transition_enter = meta_data["transition_enter"]
        mock_meta.transition_leave = meta_data["transition_leave"]
        mock_meta.is_hidden_tag = meta_data["is_hidden_tag"]
        mock_meta.fixed_tag = meta_data["fixed_tag"]
        mock_meta.dynamic_level = meta_data["dynamic_level"]
        mock_meta.created_time = "2023-01-01T00:00:00Z"
        mock_meta.updated_time = "2023-01-01T00:00:00Z"
        
        # 设置mock行为
        with patch('app.application.services.menu_meta_service.MenuMeta') as mock_menu_meta_class:
            mock_menu_meta_class.return_value = mock_meta
            mock_meta.save.return_value = None
            
            result = self.menu_meta_service.create_menu_meta(**meta_data)
            
            # 验证结果
            self.assertEqual(result["title"], meta_data["title"])
            self.assertEqual(result["icon"], meta_data["icon"])
            self.assertEqual(result["r_svg_name"], meta_data["r_svg_name"])

    def test_get_menu_meta_success(self):
        """测试成功获取菜单元数据"""
        meta_id = str(uuid.uuid4())
        mock_meta = Mock(spec=MenuMeta)
        mock_meta.id = meta_id
        mock_meta.title = "测试菜单"
        mock_meta.icon = "test-icon"
        mock_meta.r_svg_name = "test-svg"
        mock_meta.is_show_menu = True
        mock_meta.is_show_parent = True
        mock_meta.is_keepalive = True
        mock_meta.frame_url = "https://example.com"
        mock_meta.frame_loading = False
        mock_meta.transition_enter = "slide-in"
        mock_meta.transition_leave = "slide-out"
        mock_meta.is_hidden_tag = False
        mock_meta.fixed_tag = True
        mock_meta.dynamic_level = 1
        mock_meta.created_time = "2023-01-01T00:00:00Z"
        mock_meta.updated_time = "2023-01-01T00:00:00Z"
        
        # 设置mock行为
        with patch('app.application.services.menu_meta_service.MenuMeta.objects.get') as mock_get:
            mock_get.return_value = mock_meta
            
            result = self.menu_meta_service.get_menu_meta(meta_id)
            
            self.assertEqual(result["id"], meta_id)
            self.assertEqual(result["title"], "测试菜单")
            mock_get.assert_called_once_with(id=meta_id)

    def test_get_menu_meta_not_found(self):
        """测试获取不存在的菜单元数据"""
        meta_id = str(uuid.uuid4())
        
        # 设置mock行为，模拟菜单元数据不存在
        with patch('app.application.services.menu_meta_service.MenuMeta.objects.get') as mock_get:
            mock_get.side_effect = MenuMeta.DoesNotExist
            
            with self.assertRaises(BusinessException) as context:
                self.menu_meta_service.get_menu_meta(meta_id)
            
            self.assertIn("not found", str(context.exception))

    def test_update_menu_meta_success(self):
        """测试成功更新菜单元数据"""
        meta_id = str(uuid.uuid4())
        mock_meta = Mock(spec=MenuMeta)
        mock_meta.id = meta_id
        mock_meta.title = "原始标题"
        mock_meta.icon = "original-icon"
        mock_meta.r_svg_name = "original-svg"
        mock_meta.is_show_menu = True
        mock_meta.is_show_parent = True
        mock_meta.is_keepalive = True
        mock_meta.frame_url = "https://original.com"
        mock_meta.frame_loading = False
        mock_meta.transition_enter = "slide-in"
        mock_meta.transition_leave = "slide-out"
        mock_meta.is_hidden_tag = False
        mock_meta.fixed_tag = True
        mock_meta.dynamic_level = 1
        mock_meta.created_time = "2023-01-01T00:00:00Z"
        mock_meta.updated_time = "2023-01-01T00:00:00Z"
        mock_meta.save.return_value = None
        
        update_data = {
            "title": "更新标题",
            "icon": "updated-icon",
            "r_svg_name": "updated-svg",
            "is_show_menu": False,
            "is_show_parent": False,
            "is_keepalive": False,
            "frame_url": "https://updated.com",
            "frame_loading": True,
            "transition_enter": "fade-in",
            "transition_leave": "fade-out",
            "is_hidden_tag": True,
            "fixed_tag": False,
            "dynamic_level": 2
        }
        
        # 设置mock行为
        with patch('app.application.services.menu_meta_service.MenuMeta.objects.get') as mock_get:
            mock_get.return_value = mock_meta
            
            result = self.menu_meta_service.update_menu_meta(meta_id, **update_data)
            
            self.assertEqual(result["title"], update_data["title"])
            self.assertEqual(result["icon"], update_data["icon"])
            self.assertEqual(result["r_svg_name"], update_data["r_svg_name"])

    def test_update_menu_meta_not_found(self):
        """测试更新不存在的菜单元数据"""
        meta_id = str(uuid.uuid4())
        
        # 设置mock行为，模拟菜单元数据不存在
        with patch('app.application.services.menu_meta_service.MenuMeta.objects.get') as mock_get:
            mock_get.side_effect = MenuMeta.DoesNotExist
            
            with self.assertRaises(BusinessException) as context:
                self.menu_meta_service.update_menu_meta(meta_id, title="新标题")
            
            self.assertIn("not found", str(context.exception))

    def test_delete_menu_meta_success(self):
        """测试成功删除菜单元数据"""
        meta_id = str(uuid.uuid4())
        mock_meta = Mock(spec=MenuMeta)
        mock_meta.delete.return_value = None
        
        # 设置mock行为
        with patch('app.application.services.menu_meta_service.MenuMeta.objects.get') as mock_get:
            mock_get.return_value = mock_meta
            
            result = self.menu_meta_service.delete_menu_meta(meta_id)
            
            self.assertTrue(result)
            mock_meta.delete.assert_called_once()

    def test_delete_menu_meta_not_found(self):
        """测试删除不存在的菜单元数据"""
        meta_id = str(uuid.uuid4())
        
        # 设置mock行为，模拟菜单元数据不存在
        with patch('app.application.services.menu_meta_service.MenuMeta.objects.get') as mock_get:
            mock_get.side_effect = MenuMeta.DoesNotExist
            
            with self.assertRaises(BusinessException) as context:
                self.menu_meta_service.delete_menu_meta(meta_id)
            
            self.assertIn("not found", str(context.exception))

    def test_list_menu_metas(self):
        """测试获取菜单元数据列表"""
        mock_metas = []
        for i in range(3):
            mock_meta = Mock(spec=MenuMeta)
            mock_meta.id = str(uuid.uuid4())
            mock_meta.title = f"菜单{i}"
            mock_meta.icon = f"icon{i}"
            mock_meta.r_svg_name = f"svg{i}"
            mock_meta.is_show_menu = i % 2 == 0
            mock_meta.is_show_parent = i % 2 == 0
            mock_meta.is_keepalive = i % 2 == 0
            mock_meta.frame_url = f"https://example{i}.com"
            mock_meta.frame_loading = i % 2 == 0
            mock_meta.transition_enter = f"enter{i}"
            mock_meta.transition_leave = f"leave{i}"
            mock_meta.is_hidden_tag = i % 2 == 0
            mock_meta.fixed_tag = i % 2 == 0
            mock_meta.dynamic_level = i
            mock_meta.created_time = "2023-01-01T00:00:00Z"
            mock_meta.updated_time = "2023-01-01T00:00:00Z"
            mock_metas.append(mock_meta)
        
        # 设置mock行为
        with patch('app.application.services.menu_meta_service.MenuMeta.objects.all') as mock_all:
            mock_all.return_value = mock_metas
            
            result = self.menu_meta_service.list_menu_metas()
            
            self.assertEqual(len(result), 3)
            self.assertEqual(result[0]["title"], "菜单0")