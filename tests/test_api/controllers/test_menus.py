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
    
    @patch('app.application.services.menu_service.Menu')
    @patch('app.application.services.menu_service.MenuMeta')
    def test_create_menu_success(self, mock_menu_meta_class, mock_menu_class):
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
        mock_menu_class.objects.filter.return_value = mock_queryset
        
        # Mock MenuMeta.objects.get to return a mock meta
        mock_meta = Mock(spec=MenuMeta)
        mock_menu_meta_class.objects.get.return_value = mock_meta
        
        # Mock Menu constructor and save method
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
        
        # Mock the Menu class to return our mock instance when instantiated
        mock_menu_class.return_value = mock_menu_instance
        
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
        mock_menu_class.assert_called_once_with(
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
    
    @patch('app.application.services.menu_service.Menu')
    def test_get_menu_success(self, mock_menu_class):
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
        
        mock_menu_class.objects.get.return_value = mock_menu
        
        # Act
        result = self.service.get_menu(menu_id)
        
        # Assert
        self.assertEqual(result["name"], name)
        self.assertEqual(result["path"], path)
        mock_menu_class.objects.get.assert_called_once_with(id=menu_id)
    
    @patch('app.application.services.menu_service.Menu')
    def test_list_menus_success(self, mock_menu_class):
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
        mock_menu_class.objects.all.return_value = [mock_menu1, mock_menu2]
        
        # Act
        result = self.service.list_menus()
        
        # Assert
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["name"], "Dashboard")
        self.assertEqual(result[1]["name"], "Users")
    
    @patch('app.application.services.menu_service.Menu')
    @patch('app.application.services.menu_service.MenuMeta')
    def test_update_menu_success(self, mock_menu_meta_class, mock_menu_class):
        # Arrange
        menu_id = "menu123"
        menu_type = 1
        name = "Updated Dashboard"
        rank = 2
        
        # Mock Menu.objects.get to return a mock menu
        mock_menu = Mock(spec=Menu)
        mock_menu.menu_type = 1
        mock_menu.name = "Dashboard"
        mock_menu.rank = 1
        mock_menu.meta_id = "meta123"
        mock_menu.save.return_value = None
        
        mock_menu_class.objects.get.return_value = mock_menu
        
        # Mock Menu.objects.filter to return empty queryset (no existing menu with new name)
        mock_queryset = Mock()
        mock_queryset.exists.return_value = False
        mock_queryset.exclude.return_value = mock_queryset
        mock_menu_class.objects.filter.return_value = mock_queryset
        
        # Mock MenuMeta.objects.get to return a mock meta
        mock_meta = Mock(spec=MenuMeta)
        mock_menu_meta_class.objects.get.return_value = mock_meta
        
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
        mock_menu_class.objects.get.assert_called_once_with(id=menu_id)
        mock_menu.save.assert_called_once()
    
    @patch('app.application.services.menu_service.Menu')
    def test_delete_menu_success(self, mock_menu_class):
        # Arrange
        menu_id = "menu123"
        
        # Mock Menu.objects.get to return a mock menu
        mock_menu = Mock(spec=Menu)
        mock_menu.delete.return_value = None
        
        mock_menu_class.objects.get.return_value = mock_menu
        
        # Act
        result = self.service.delete_menu(menu_id)
        
        # Assert
        self.assertTrue(result)
        mock_menu_class.objects.get.assert_called_once_with(id=menu_id)
        mock_menu.delete.assert_called_once()
    
    @patch('app.application.services.menu_service.Menu')
    def test_get_menu_not_found(self, mock_menu_class):
        # Arrange
        menu_id = "menu123"
        
        # Mock Menu.objects.get to raise DoesNotExist
        mock_menu_class.DoesNotExist = Exception
        mock_menu_class.objects.get.side_effect = mock_menu_class.DoesNotExist("Menu does not exist")
        
        # Act & Assert
        with self.assertRaises(BusinessException):
            self.service.get_menu(menu_id)
    
    @patch('app.application.services.menu_service.Menu')
    def test_update_menu_not_found(self, mock_menu_class):
        # Arrange
        menu_id = "menu123"
        name = "Updated Dashboard"
        
        # Mock Menu.objects.get to raise DoesNotExist
        mock_menu_class.DoesNotExist = Exception
        mock_menu_class.objects.get.side_effect = mock_menu_class.DoesNotExist("Menu does not exist")
        
        # Act & Assert
        with self.assertRaises(BusinessException):
            self.service.update_menu(menu_id=menu_id, name=name)
    
    @patch('app.application.services.menu_service.Menu')
    def test_delete_menu_not_found(self, mock_menu_class):
        # Arrange
        menu_id = "menu123"
        
        # Mock Menu.objects.get to raise DoesNotExist
        mock_menu_class.DoesNotExist = Exception
        mock_menu_class.objects.get.side_effect = mock_menu_class.DoesNotExist("Menu does not exist")
        
        # Act & Assert
        with self.assertRaises(BusinessException):
            self.service.delete_menu(menu_id)
    
    @patch('app.application.services.menu_service.Menu')
    def test_create_menu_name_exists(self, mock_menu_class):
        # Arrange
        menu_type = 1
        name = "Dashboard"
        rank = 1
        
        # Mock Menu.objects.filter to return queryset that exists (menu with this name already exists)
        mock_queryset = Mock()
        mock_queryset.exists.return_value = True
        mock_menu_class.objects.filter.return_value = mock_queryset
        
        # Act & Assert
        with self.assertRaises(BusinessException):
            self.service.create_menu(
                menu_type=menu_type,
                name=name,
                rank=rank
            )