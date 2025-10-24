"""
测试菜单应用服务
"""

from django.test import TestCase
from app.application.services.menu_service import MenuService
from app.domain.models.menu import Menu
from app.domain.models.menu_meta import MenuMeta
from app.common.exception.exceptions import BusinessException
from unittest.mock import Mock, patch
import uuid


class TestMenuService(TestCase):
    def setUp(self):
        """测试初始化"""
        self.menu_service = MenuService()

    def test_create_menu_success(self):
        """测试成功创建菜单"""
        # 准备测试数据
        menu_data = {
            "menu_type": 1,
            "name": "测试菜单",
            "rank": 1,
            "path": "/test",
            "component": "TestComponent",
            "is_active": True,
            "method": "GET",
            "parent_id": None,
            "meta_id": str(uuid.uuid4())
        }
        
        # 创建mock的menu对象
        mock_menu = Mock(spec=Menu)
        mock_menu.id = str(uuid.uuid4())
        mock_menu.menu_type = menu_data["menu_type"]
        mock_menu.name = menu_data["name"]
        mock_menu.rank = menu_data["rank"]
        mock_menu.path = menu_data["path"]
        mock_menu.component = menu_data["component"]
        mock_menu.is_active = menu_data["is_active"]
        mock_menu.method = menu_data["method"]
        mock_menu.parent_id = menu_data["parent_id"]
        mock_menu.meta_id = menu_data["meta_id"]
        mock_menu.created_time = "2023-01-01T00:00:00Z"
        mock_menu.updated_time = "2023-01-01T00:00:00Z"
        
        # 设置mock行为
        with patch('app.application.services.menu_service.Menu') as mock_menu_class:
            with patch('app.application.services.menu_service.MenuMeta') as mock_menu_meta_class:
                # 模拟name不存在
                mock_menu_class.objects.filter.return_value.exists.return_value = False
                # 模拟meta存在
                mock_menu_meta_class.objects.get.return_value = Mock(spec=MenuMeta)
                mock_menu_class.return_value = mock_menu
                mock_menu.save.return_value = None
                
                result = self.menu_service.create_menu(**menu_data)
                
                # 验证结果
                self.assertEqual(result["name"], menu_data["name"])
                self.assertEqual(result["menu_type"], menu_data["menu_type"])
                self.assertEqual(result["path"], menu_data["path"])

    def test_create_menu_duplicate_name(self):
        """测试创建菜单时name重复"""
        menu_data = {
            "menu_type": 1,
            "name": "重复菜单",
            "rank": 1,
            "path": "/test",
            "component": "TestComponent",
            "is_active": True,
            "method": "GET"
        }
        
        # 设置mock行为，模拟name已存在
        with patch('app.application.services.menu_service.Menu') as mock_menu_class:
            mock_menu_class.objects.filter.return_value.exists.return_value = True
            
            with self.assertRaises(BusinessException) as context:
                self.menu_service.create_menu(**menu_data)
            
            self.assertIn("already exists", str(context.exception))

    def test_create_menu_meta_not_found(self):
        """测试创建菜单时meta不存在"""
        menu_data = {
            "menu_type": 1,
            "name": "测试菜单",
            "rank": 1,
            "path": "/test",
            "component": "TestComponent",
            "is_active": True,
            "method": "GET",
            "meta_id": str(uuid.uuid4())
        }
        
        # 设置mock行为，模拟meta不存在
        with patch('app.application.services.menu_service.Menu') as mock_menu_class:
            with patch('app.application.services.menu_service.MenuMeta') as mock_menu_meta_class:
                mock_menu_class.objects.filter.return_value.exists.return_value = False
                mock_menu_meta_class.objects.get.side_effect = MenuMeta.DoesNotExist
                
                with self.assertRaises(BusinessException) as context:
                    self.menu_service.create_menu(**menu_data)
                
                self.assertIn("not found", str(context.exception))

    def test_get_menu_success(self):
        """测试成功获取菜单"""
        menu_id = str(uuid.uuid4())
        mock_menu = Mock(spec=Menu)
        mock_menu.id = menu_id
        mock_menu.menu_type = 1
        mock_menu.name = "测试菜单"
        mock_menu.rank = 1
        mock_menu.path = "/test"
        mock_menu.component = "TestComponent"
        mock_menu.is_active = True
        mock_menu.method = "GET"
        mock_menu.parent_id = None
        mock_menu.meta_id = str(uuid.uuid4())
        mock_menu.created_time = "2023-01-01T00:00:00Z"
        mock_menu.updated_time = "2023-01-01T00:00:00Z"
        
        # 设置mock行为
        with patch('app.application.services.menu_service.Menu.objects.get') as mock_get:
            mock_get.return_value = mock_menu
            
            result = self.menu_service.get_menu(menu_id)
            
            self.assertEqual(result["id"], menu_id)
            self.assertEqual(result["name"], "测试菜单")
            mock_get.assert_called_once_with(id=menu_id)

    def test_get_menu_not_found(self):
        """测试获取不存在的菜单"""
        menu_id = str(uuid.uuid4())
        
        # 设置mock行为，模拟菜单不存在
        with patch('app.application.services.menu_service.Menu.objects.get') as mock_get:
            mock_get.side_effect = Menu.DoesNotExist
            
            with self.assertRaises(BusinessException) as context:
                self.menu_service.get_menu(menu_id)
            
            self.assertIn("not found", str(context.exception))

    def test_update_menu_success(self):
        """测试成功更新菜单"""
        menu_id = str(uuid.uuid4())
        mock_menu = Mock(spec=Menu)
        mock_menu.id = menu_id
        mock_menu.menu_type = 1
        mock_menu.name = "原始菜单"
        mock_menu.rank = 1
        mock_menu.path = "/original"
        mock_menu.component = "OriginalComponent"
        mock_menu.is_active = True
        mock_menu.method = "GET"
        mock_menu.parent_id = None
        mock_menu.meta_id = str(uuid.uuid4())
        mock_menu.created_time = "2023-01-01T00:00:00Z"
        mock_menu.updated_time = "2023-01-01T00:00:00Z"
        mock_menu.save.return_value = None
        
        update_data = {
            "menu_type": 2,
            "name": "更新菜单",
            "rank": 2,
            "path": "/updated",
            "component": "UpdatedComponent",
            "is_active": False,
            "method": "POST",
            "parent_id": str(uuid.uuid4()),
            "meta_id": str(uuid.uuid4())
        }
        
        # 设置mock行为
        with patch('app.application.services.menu_service.Menu.objects.get') as mock_get:
            with patch('app.application.services.menu_service.MenuMeta') as mock_menu_meta_class:
                # 模拟新name不存在（排除当前菜单）
                with patch('app.application.services.menu_service.Menu') as mock_menu_class:
                    mock_menu_class.objects.filter.return_value.exclude.return_value.exists.return_value = False
                    mock_menu_meta_class.objects.get.return_value = Mock(spec=MenuMeta)
                    mock_get.return_value = mock_menu
                    
                    result = self.menu_service.update_menu(menu_id, **update_data)
                    
                    self.assertEqual(result["name"], update_data["name"])
                    self.assertEqual(result["menu_type"], update_data["menu_type"])
                    self.assertEqual(result["path"], update_data["path"])

    def test_update_menu_not_found(self):
        """测试更新不存在的菜单"""
        menu_id = str(uuid.uuid4())
        
        # 设置mock行为，模拟菜单不存在
        with patch('app.application.services.menu_service.Menu.objects.get') as mock_get:
            mock_get.side_effect = Menu.DoesNotExist
            
            with self.assertRaises(BusinessException) as context:
                self.menu_service.update_menu(menu_id, name="新菜单")
            
            self.assertIn("not found", str(context.exception))

    def test_update_menu_duplicate_name(self):
        """测试更新菜单时name重复"""
        menu_id = str(uuid.uuid4())
        
        # 设置mock行为，模拟name已存在（排除当前菜单）
        with patch('app.application.services.menu_service.Menu.objects.get') as mock_get:
            with patch('app.application.services.menu_service.Menu') as mock_menu_class:
                mock_menu_class.objects.filter.return_value.exclude.return_value.exists.return_value = True
                mock_get.return_value = Mock(spec=Menu)
                
                with self.assertRaises(BusinessException) as context:
                    self.menu_service.update_menu(menu_id, name="重复菜单")
                
                self.assertIn("already exists", str(context.exception))

    def test_update_menu_meta_not_found(self):
        """测试更新菜单时meta不存在"""
        menu_id = str(uuid.uuid4())
        
        # 设置mock行为，模拟meta不存在
        with patch('app.application.services.menu_service.Menu.objects.get') as mock_get:
            with patch('app.application.services.menu_service.MenuMeta') as mock_menu_meta_class:
                mock_get.return_value = Mock(spec=Menu)
                mock_menu_meta_class.objects.get.side_effect = MenuMeta.DoesNotExist
                
                with self.assertRaises(BusinessException) as context:
                    self.menu_service.update_menu(menu_id, meta_id=str(uuid.uuid4()))
                
                self.assertIn("not found", str(context.exception))

    def test_delete_menu_success(self):
        """测试成功删除菜单"""
        menu_id = str(uuid.uuid4())
        mock_menu = Mock(spec=Menu)
        mock_menu.delete.return_value = None
        
        # 设置mock行为
        with patch('app.application.services.menu_service.Menu.objects.get') as mock_get:
            mock_get.return_value = mock_menu
            
            result = self.menu_service.delete_menu(menu_id)
            
            self.assertTrue(result)
            mock_menu.delete.assert_called_once()

    def test_delete_menu_not_found(self):
        """测试删除不存在的菜单"""
        menu_id = str(uuid.uuid4())
        
        # 设置mock行为，模拟菜单不存在
        with patch('app.application.services.menu_service.Menu.objects.get') as mock_get:
            mock_get.side_effect = Menu.DoesNotExist
            
            with self.assertRaises(BusinessException) as context:
                self.menu_service.delete_menu(menu_id)
            
            self.assertIn("not found", str(context.exception))

    def test_list_menus(self):
        """测试获取菜单列表"""
        mock_menus = []
        for i in range(3):
            mock_menu = Mock(spec=Menu)
            mock_menu.id = str(uuid.uuid4())
            mock_menu.menu_type = i + 1
            mock_menu.name = f"菜单{i}"
            mock_menu.rank = i
            mock_menu.path = f"/menu{i}"
            mock_menu.component = f"Component{i}"
            mock_menu.is_active = i % 2 == 0
            mock_menu.method = "GET" if i % 2 == 0 else "POST"
            mock_menu.parent_id = None if i < 2 else str(uuid.uuid4())
            mock_menu.meta_id = str(uuid.uuid4()) if i > 0 else None
            mock_menu.created_time = "2023-01-01T00:00:00Z"
            mock_menu.updated_time = "2023-01-01T00:00:00Z"
            mock_menus.append(mock_menu)
        
        # 设置mock行为
        with patch('app.application.services.menu_service.Menu.objects.all') as mock_all:
            mock_all.return_value = mock_menus
            
            result = self.menu_service.list_menus()
            
            self.assertEqual(len(result), 3)
            self.assertEqual(result[0]["name"], "菜单0")