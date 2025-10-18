# test_menu_metas_controller.py
from unittest.mock import Mock, patch
from django.test import TestCase
from app.application.services.menu_meta_service import MenuMetaService
from app.domain.models.menu_meta import MenuMeta
from app.common.exception.exceptions import BusinessException
from datetime import datetime


class TestMenuMetasController(TestCase):
    def setUp(self):
        self.service = MenuMetaService()
    
    def test_create_menu_meta_success(self):
        # Arrange
        title = "Dashboard Meta"
        icon = "dashboard-icon"
        is_show_menu = True
        is_show_parent = True
        is_keepalive = True
        
        # Mock MenuMeta constructor and save method
        with patch('app.domain.models.menu_meta.MenuMeta') as MockMenuMeta:
            mock_menu_meta_instance = Mock(spec=MenuMeta)
            mock_menu_meta_instance.id = "meta123"
            mock_menu_meta_instance.title = title
            mock_menu_meta_instance.icon = icon
            mock_menu_meta_instance.is_show_menu = is_show_menu
            mock_menu_meta_instance.is_show_parent = is_show_parent
            mock_menu_meta_instance.is_keepalive = is_keepalive
            mock_menu_meta_instance.created_time = datetime.now()
            mock_menu_meta_instance.updated_time = datetime.now()
            
            MockMenuMeta.return_value = mock_menu_meta_instance
            mock_menu_meta_instance.save.return_value = None
            
            # Act
            result = self.service.create_menu_meta(
                title=title,
                icon=icon,
                is_show_menu=is_show_menu,
                is_show_parent=is_show_parent,
                is_keepalive=is_keepalive
            )
            
            # Assert
            self.assertEqual(result["title"], title)
            self.assertEqual(result["icon"], icon)
            MockMenuMeta.assert_called_once_with(
                title=title,
                icon=icon,
                r_svg_name=None,
                is_show_menu=is_show_menu,
                is_show_parent=is_show_parent,
                is_keepalive=is_keepalive,
                frame_url=None,
                frame_loading=False,
                transition_enter=None,
                transition_leave=None,
                is_hidden_tag=False,
                fixed_tag=False,
                dynamic_level=0
            )
            mock_menu_meta_instance.save.assert_called_once()
    
    def test_get_menu_meta_success(self):
        # Arrange
        menu_meta_id = "meta123"
        title = "Dashboard Meta"
        icon = "dashboard-icon"
        is_show_menu = True
        is_show_parent = True
        is_keepalive = True
        
        # Mock MenuMeta.objects.get to return a mock menu meta
        with patch('app.domain.models.menu_meta.MenuMeta.objects.get') as mock_menu_meta_get:
            mock_menu_meta = Mock(spec=MenuMeta)
            mock_menu_meta.id = menu_meta_id
            mock_menu_meta.title = title
            mock_menu_meta.icon = icon
            mock_menu_meta.is_show_menu = is_show_menu
            mock_menu_meta.is_show_parent = is_show_parent
            mock_menu_meta.is_keepalive = is_keepalive
            mock_menu_meta.created_time = datetime.now()
            mock_menu_meta.updated_time = datetime.now()
            
            mock_menu_meta_get.return_value = mock_menu_meta
            
            # Act
            result = self.service.get_menu_meta(menu_meta_id)
            
            # Assert
            self.assertEqual(result["title"], title)
            self.assertEqual(result["icon"], icon)
            mock_menu_meta_get.assert_called_once_with(id=menu_meta_id)
    
    def test_list_menu_metas_success(self):
        # Arrange
        # Create mock menu meta objects
        mock_menu_meta1 = Mock(spec=MenuMeta)
        mock_menu_meta1.id = "meta123"
        mock_menu_meta1.title = "Dashboard Meta"
        mock_menu_meta1.icon = "dashboard-icon"
        mock_menu_meta1.is_show_menu = True
        mock_menu_meta1.is_show_parent = True
        mock_menu_meta1.is_keepalive = True
        mock_menu_meta1.created_time = datetime.now()
        mock_menu_meta1.updated_time = datetime.now()
        
        mock_menu_meta2 = Mock(spec=MenuMeta)
        mock_menu_meta2.id = "meta456"
        mock_menu_meta2.title = "Users Meta"
        mock_menu_meta2.icon = "users-icon"
        mock_menu_meta2.is_show_menu = True
        mock_menu_meta2.is_show_parent = True
        mock_menu_meta2.is_keepalive = True
        mock_menu_meta2.created_time = datetime.now()
        mock_menu_meta2.updated_time = datetime.now()
        
        # Mock MenuMeta.objects.all to return the mock menu metas
        with patch('app.domain.models.menu_meta.MenuMeta.objects.all', return_value=[mock_menu_meta1, mock_menu_meta2]):
            # Act
            result = self.service.list_menu_metas()
            
            # Assert
            self.assertEqual(len(result), 2)
            self.assertEqual(result[0]["title"], "Dashboard Meta")
            self.assertEqual(result[1]["title"], "Users Meta")
    
    def test_update_menu_meta_success(self):
        # Arrange
        menu_meta_id = "meta123"
        title = "Updated Dashboard Meta"
        icon = "updated-dashboard-icon"
        
        # Mock MenuMeta.objects.get to return a mock menu meta
        with patch('app.domain.models.menu_meta.MenuMeta.objects.get') as mock_menu_meta_get:
            mock_menu_meta = Mock(spec=MenuMeta)
            mock_menu_meta.title = "Dashboard Meta"
            mock_menu_meta.icon = "dashboard-icon"
            
            mock_menu_meta_get.return_value = mock_menu_meta
            mock_menu_meta.save.return_value = None
            
            # Act
            result = self.service.update_menu_meta(
                menu_meta_id=menu_meta_id,
                title=title,
                icon=icon
            )
            
            # Assert
            self.assertEqual(result["title"], title)
            self.assertEqual(result["icon"], icon)
            mock_menu_meta_get.assert_called_once_with(id=menu_meta_id)
            mock_menu_meta.save.assert_called_once()
    
    def test_delete_menu_meta_success(self):
        # Arrange
        menu_meta_id = "meta123"
        
        # Mock MenuMeta.objects.get to return a mock menu meta
        with patch('app.domain.models.menu_meta.MenuMeta.objects.get') as mock_menu_meta_get:
            mock_menu_meta = Mock(spec=MenuMeta)
            mock_menu_meta.delete.return_value = None
            
            mock_menu_meta_get.return_value = mock_menu_meta
            
            # Act
            result = self.service.delete_menu_meta(menu_meta_id)
            
            # Assert
            self.assertTrue(result)
            mock_menu_meta_get.assert_called_once_with(id=menu_meta_id)
            mock_menu_meta.delete.assert_called_once()
    
    def test_get_menu_meta_not_found(self):
        # Arrange
        menu_meta_id = "meta123"
        
        # Mock MenuMeta.objects.get to raise DoesNotExist
        with patch('app.domain.models.menu_meta.MenuMeta.objects.get') as mock_menu_meta_get:
            # 创建一个DoesNotExist异常实例
            does_not_exist_exception = Exception("MenuMeta does not exist")
            mock_menu_meta_get.side_effect = does_not_exist_exception
            
            # Act & Assert
            with self.assertRaises(BusinessException):
                self.service.get_menu_meta(menu_meta_id)
    
    def test_update_menu_meta_not_found(self):
        # Arrange
        menu_meta_id = "meta123"
        title = "Updated Dashboard Meta"
        
        # Mock MenuMeta.objects.get to raise DoesNotExist
        with patch('app.domain.models.menu_meta.MenuMeta.objects.get') as mock_menu_meta_get:
            # 创建一个DoesNotExist异常实例
            does_not_exist_exception = Exception("MenuMeta does not exist")
            mock_menu_meta_get.side_effect = does_not_exist_exception
            
            # Act & Assert
            with self.assertRaises(BusinessException):
                self.service.update_menu_meta(menu_meta_id=menu_meta_id, title=title)
    
    def test_delete_menu_meta_not_found(self):
        # Arrange
        menu_meta_id = "meta123"
        
        # Mock MenuMeta.objects.get to raise DoesNotExist
        with patch('app.domain.models.menu_meta.MenuMeta.objects.get') as mock_menu_meta_get:
            # 创建一个DoesNotExist异常实例
            does_not_exist_exception = Exception("MenuMeta does not exist")
            mock_menu_meta_get.side_effect = does_not_exist_exception
            
            # Act & Assert
            with self.assertRaises(BusinessException):
                self.service.delete_menu_meta(menu_meta_id)