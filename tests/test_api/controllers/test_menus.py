# test_menus_controller.py
from unittest.mock import Mock, patch
from django.test import TestCase
from app.application.services.menu_service import MenuService
from app.domain.models.menu import Menu
from app.domain.models.menu_meta import MenuMeta
from app.common.exception.exceptions import BusinessException
from datetime import datetime


class TestMenusController(TestCase):
    def setUp(self):
        self.service = MenuService()
    
    def test_create_menu_success(self):
        # Arrange
        menu_type = 1
        name = "Dashboard"
        rank = 1
        path = "/dashboard"
        component = "Dashboard.vue"
        is_active = True
        method = "GET"
        parent_id = None
        meta_id = "meta123"
        
        # Mock Menu.objects.filter to return empty queryset (no existing menu with this name)
        mock_queryset = Mock()
        mock_queryset.exists.return_value = False
        with patch('app.domain.models.menu.Menu.objects.filter', return_value=mock_queryset):
            # Mock MenuMeta.objects.get to return a mock meta
            with patch('app.domain.models.menu_meta.MenuMeta.objects.get') as mock_meta_get:
                mock_meta = Mock(spec=MenuMeta)
                mock_meta_get.return_value = mock_meta
                
                # Mock Menu constructor and save method
                with patch('app.domain.models.menu.Menu') as MockMenu:
                    mock_menu_instance = Mock(spec=Menu)
                    mock_menu_instance.id = "menu123"
                    mock_menu_instance.menu_type = menu_type
                    mock_menu_instance.name = name
                    mock_menu_instance.rank = rank
                    mock_menu_instance.path = path
                    mock_menu_instance.component = component
                    mock_menu_instance.is_active = is_active
                    mock_menu_instance.method = method
                    mock_menu_instance.parent_id = parent_id
                    mock_menu_instance.meta_id = meta_id
                    mock_menu_instance.created_time = datetime.now()
                    mock_menu_instance.updated_time = datetime.now()
                    
                    MockMenu.return_value = mock_menu_instance
                    mock_menu_instance.save.return_value = None
                    
                    # Act
                    result = self.service.create_menu(
                        menu_type=menu_type,
                        name=name,
                        rank=rank,
                        path=path,
                        component=component,
                        is_active=is_active,
                        method=method,
                        parent_id=parent_id,
                        meta_id=meta_id
                    )
                    
                    # Assert
                    self.assertEqual(result["name"], name)
                    self.assertEqual(result["path"], path)
                    MockMenu.assert_called_once_with(
                        menu_type=menu_type,
                        name=name,
                        rank=rank,
                        path=path,
                        component=component,
                        is_active=is_active,
                        method=method,
                        meta_id=meta_id,
                        parent_id=parent_id
                    )
                    mock_menu_instance.save.assert_called_once()
    
    def test_get_menu_success(self):
        # Arrange
        menu_id = "menu123"
        menu_type = 1
        name = "Dashboard"
        rank = 1
        path = "/dashboard"
        component = "Dashboard.vue"
        is_active = True
        method = "GET"
        parent_id = None
        meta_id = "meta123"
        
        # Mock Menu.objects.get to return a mock menu
        with patch('app.domain.models.menu.Menu.objects.get') as mock_menu_get:
            mock_menu = Mock(spec=Menu)
            mock_menu.id = menu_id
            mock_menu.menu_type = menu_type
            mock_menu.name = name
            mock_menu.rank = rank
            mock_menu.path = path
            mock_menu.component = component
            mock_menu.is_active = is_active
            mock_menu.method = method
            mock_menu.parent_id = parent_id
            mock_menu.meta_id = meta_id
            mock_menu.created_time = datetime.now()
            mock_menu.updated_time = datetime.now()
            
            mock_menu_get.return_value = mock_menu
            
            # Act
            result = self.service.get_menu(menu_id)
            
            # Assert
            self.assertEqual(result["name"], name)
            self.assertEqual(result["path"], path)
            mock_menu_get.assert_called_once_with(id=menu_id)
    
    def test_list_menus_success(self):
        # Arrange
        # Create mock menu objects
        mock_menu1 = Mock(spec=Menu)
        mock_menu1.id = "menu123"
        mock_menu1.menu_type = 1
        mock_menu1.name = "Dashboard"
        mock_menu1.rank = 1
        mock_menu1.path = "/dashboard"
        mock_menu1.component = "Dashboard.vue"
        mock_menu1.is_active = True
        mock_menu1.method = "GET"
        mock_menu1.parent_id = None
        mock_menu1.meta_id = "meta123"
        mock_menu1.created_time = datetime.now()
        mock_menu1.updated_time = datetime.now()
        
        mock_menu2 = Mock(spec=Menu)
        mock_menu2.id = "menu456"
        mock_menu2.menu_type = 2
        mock_menu2.name = "Users"
        mock_menu2.rank = 2
        mock_menu2.path = "/users"
        mock_menu2.component = "Users.vue"
        mock_menu2.is_active = True
        mock_menu2.method = "GET"
        mock_menu2.parent_id = None
        mock_menu2.meta_id = "meta456"
        mock_menu2.created_time = datetime.now()
        mock_menu2.updated_time = datetime.now()
        
        # Mock Menu.objects.all to return the mock menus
        with patch('app.domain.models.menu.Menu.objects.all', return_value=[mock_menu1, mock_menu2]):
            # Act
            result = self.service.list_menus()
            
            # Assert
            self.assertEqual(len(result), 2)
            self.assertEqual(result[0]["name"], "Dashboard")
            self.assertEqual(result[1]["name"], "Users")
    
    def test_update_menu_success(self):
        # Arrange
        menu_id = "menu123"
        menu_type = 1
        name = "Updated Dashboard"
        rank = 2
        
        # Mock Menu.objects.get to return a mock menu
        with patch('app.domain.models.menu.Menu.objects.get') as mock_menu_get:
            mock_menu = Mock(spec=Menu)
            mock_menu.menu_type = 1
            mock_menu.name = "Dashboard"
            mock_menu.rank = 1
            mock_menu.meta_id = "meta123"
            
            mock_menu_get.return_value = mock_menu
            
            # Mock Menu.objects.filter to return empty queryset (no existing menu with new name)
            mock_queryset = Mock()
            mock_queryset.exists.return_value = False
            mock_queryset.exclude.return_value = mock_queryset
            with patch('app.domain.models.menu.Menu.objects.filter', return_value=mock_queryset):
                # Mock MenuMeta.objects.get to return a mock meta
                with patch('app.domain.models.menu_meta.MenuMeta.objects.get') as mock_meta_get:
                    mock_meta = Mock(spec=MenuMeta)
                    mock_meta_get.return_value = mock_meta
                    
                    mock_menu.save.return_value = None
                    
                    # Act
                    result = self.service.update_menu(
                        menu_id=menu_id,
                        menu_type=menu_type,
                        name=name,
                        rank=rank
                    )
                    
                    # Assert
                    self.assertEqual(result["name"], name)
                    self.assertEqual(result["rank"], rank)
                    mock_menu_get.assert_called_once_with(id=menu_id)
                    mock_menu.save.assert_called_once()
    
    def test_delete_menu_success(self):
        # Arrange
        menu_id = "menu123"
        
        # Mock Menu.objects.get to return a mock menu
        with patch('app.domain.models.menu.Menu.objects.get') as mock_menu_get:
            mock_menu = Mock(spec=Menu)
            mock_menu.delete.return_value = None
            
            mock_menu_get.return_value = mock_menu
            
            # Act
            result = self.service.delete_menu(menu_id)
            
            # Assert
            self.assertTrue(result)
            mock_menu_get.assert_called_once_with(id=menu_id)
            mock_menu.delete.assert_called_once()
    
    def test_create_menu_name_exists(self):
        # Arrange
        menu_type = 1
        name = "Dashboard"
        rank = 1
        
        # Mock Menu.objects.filter to return queryset that exists (menu with this name already exists)
        mock_queryset = Mock()
        mock_queryset.exists.return_value = True
        with patch('app.domain.models.menu.Menu.objects.filter', return_value=mock_queryset):
            # Act & Assert
            with self.assertRaises(BusinessException):
                self.service.create_menu(menu_type=menu_type, name=name, rank=rank)
    
    def test_get_menu_not_found(self):
        # Arrange
        menu_id = "menu123"
        
        # Mock Menu.objects.get to raise DoesNotExist
        with patch('app.domain.models.menu.Menu.objects.get') as mock_menu_get:
            # 创建一个DoesNotExist异常实例
            does_not_exist_exception = type('DoesNotExist', (Exception,), {})()
            mock_menu_get.side_effect = does_not_exist_exception
            
            # Act & Assert
            with self.assertRaises(BusinessException):
                self.service.get_menu(menu_id)
    
    def test_update_menu_not_found(self):
        # Arrange
        menu_id = "menu123"
        name = "Updated Dashboard"
        
        # Mock Menu.objects.get to raise DoesNotExist
        with patch('app.domain.models.menu.Menu.objects.get') as mock_menu_get:
            # 创建一个DoesNotExist异常实例
            does_not_exist_exception = type('DoesNotExist', (Exception,), {})()
            mock_menu_get.side_effect = does_not_exist_exception
            
            # Act & Assert
            with self.assertRaises(BusinessException):
                self.service.update_menu(menu_id=menu_id, name=name)
    
    def test_delete_menu_not_found(self):
        # Arrange
        menu_id = "menu123"
        
        # Mock Menu.objects.get to raise DoesNotExist
        with patch('app.domain.models.menu.Menu.objects.get') as mock_menu_get:
            # 创建一个DoesNotExist异常实例
            does_not_exist_exception = type('DoesNotExist', (Exception,), {})()
            mock_menu_get.side_effect = does_not_exist_exception
            
            # Act & Assert
            with self.assertRaises(BusinessException):
                self.service.delete_menu(menu_id)