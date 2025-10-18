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
    
    @patch('app.application.services.menu_meta_service.MenuMeta')
    def test_create_menu_meta_success(self, mock_menu_meta_class):
        # Arrange
        title = "Dashboard Meta"
        icon = "dashboard-icon"
        r_svg_name = "dashboard-svg"
        is_show_menu = True
        is_show_parent = True
        is_keepalive = True
        frame_url = "https://example.com"
        frame_loading = False
        transition_enter = "slide"
        transition_leave = "fade"
        is_hidden_tag = False
        fixed_tag = True
        dynamic_level = 1
        
        # Create a mock menu meta object
        mock_menu_meta_instance = Mock(spec=MenuMeta)
        mock_menu_meta_instance.id = "meta123"
        mock_menu_meta_instance.title = title
        mock_menu_meta_instance.icon = icon
        mock_menu_meta_instance.r_svg_name = r_svg_name
        mock_menu_meta_instance.is_show_menu = is_show_menu
        mock_menu_meta_instance.is_show_parent = is_show_parent
        mock_menu_meta_instance.is_keepalive = is_keepalive
        mock_menu_meta_instance.frame_url = frame_url
        mock_menu_meta_instance.frame_loading = frame_loading
        mock_menu_meta_instance.transition_enter = transition_enter
        mock_menu_meta_instance.transition_leave = transition_leave
        mock_menu_meta_instance.is_hidden_tag = is_hidden_tag
        mock_menu_meta_instance.fixed_tag = fixed_tag
        mock_menu_meta_instance.dynamic_level = dynamic_level
        mock_menu_meta_instance.created_time = datetime.now()
        mock_menu_meta_instance.updated_time = datetime.now()
        
        # Mock the MenuMeta class to return our mock instance when instantiated
        mock_menu_meta_class.return_value = mock_menu_meta_instance
        
        # Act
        result = self.service.create_menu_meta(
            title=title,
            icon=icon,
            r_svg_name=r_svg_name,
            is_show_menu=is_show_menu,
            is_show_parent=is_show_parent,
            is_keepalive=is_keepalive,
            frame_url=frame_url,
            frame_loading=frame_loading,
            transition_enter=transition_enter,
            transition_leave=transition_leave,
            is_hidden_tag=is_hidden_tag,
            fixed_tag=fixed_tag,
            dynamic_level=dynamic_level
        )
        
        # Assert
        self.assertEqual(result["title"], title)
        self.assertEqual(result["icon"], icon)
        mock_menu_meta_class.assert_called_once_with(
            title=title,
            icon=icon,
            r_svg_name=r_svg_name,
            is_show_menu=is_show_menu,
            is_show_parent=is_show_parent,
            is_keepalive=is_keepalive,
            frame_url=frame_url,
            frame_loading=frame_loading,
            transition_enter=transition_enter,
            transition_leave=transition_leave,
            is_hidden_tag=is_hidden_tag,
            fixed_tag=fixed_tag,
            dynamic_level=dynamic_level
        )
        mock_menu_meta_instance.save.assert_called_once()
    
    @patch('app.application.services.menu_meta_service.MenuMeta')
    def test_get_menu_meta_success(self, mock_menu_meta_class):
        # Arrange
        menu_meta_id = "meta123"
        title = "Dashboard Meta"
        icon = "dashboard-icon"
        r_svg_name = "dashboard-svg"
        is_show_menu = True
        is_show_parent = True
        is_keepalive = True
        frame_url = "https://example.com"
        frame_loading = False
        transition_enter = "slide"
        transition_leave = "fade"
        is_hidden_tag = False
        fixed_tag = True
        dynamic_level = 1
        
        # Mock MenuMeta.objects.get to return a mock menu meta
        mock_menu_meta_class.objects.get.return_value = Mock(
            spec=MenuMeta,
            id=menu_meta_id,
            title=title,
            icon=icon,
            r_svg_name=r_svg_name,
            is_show_menu=is_show_menu,
            is_show_parent=is_show_parent,
            is_keepalive=is_keepalive,
            frame_url=frame_url,
            frame_loading=frame_loading,
            transition_enter=transition_enter,
            transition_leave=transition_leave,
            is_hidden_tag=is_hidden_tag,
            fixed_tag=fixed_tag,
            dynamic_level=dynamic_level,
            created_time=datetime.now(),
            updated_time=datetime.now()
        )
        
        # Act
        result = self.service.get_menu_meta(menu_meta_id)
        
        # Assert
        self.assertEqual(result["title"], title)
        self.assertEqual(result["icon"], icon)
        mock_menu_meta_class.objects.get.assert_called_once_with(id=menu_meta_id)
    
    @patch('app.application.services.menu_meta_service.MenuMeta')
    def test_list_menu_metas_success(self, mock_menu_meta_class):
        # Arrange
        # Create mock menu meta objects
        mock_menu_meta1 = Mock(
            spec=MenuMeta,
            id="meta123",
            title="Dashboard Meta",
            icon="dashboard-icon",
            r_svg_name="dashboard-svg",
            is_show_menu=True,
            is_show_parent=True,
            is_keepalive=True,
            frame_url="https://example.com",
            frame_loading=False,
            transition_enter="slide",
            transition_leave="fade",
            is_hidden_tag=False,
            fixed_tag=True,
            dynamic_level=1,
            created_time=datetime.now(),
            updated_time=datetime.now()
        )
        
        mock_menu_meta2 = Mock(
            spec=MenuMeta,
            id="meta456",
            title="Users Meta",
            icon="users-icon",
            r_svg_name="users-svg",
            is_show_menu=True,
            is_show_parent=True,
            is_keepalive=True,
            frame_url="https://users.example.com",
            frame_loading=False,
            transition_enter="slide",
            transition_leave="fade",
            is_hidden_tag=False,
            fixed_tag=True,
            dynamic_level=1,
            created_time=datetime.now(),
            updated_time=datetime.now()
        )
        
        # Mock MenuMeta.objects.all to return the mock menu metas
        mock_menu_meta_class.objects.all.return_value = [mock_menu_meta1, mock_menu_meta2]
        
        # Act
        result = self.service.list_menu_metas()
        
        # Assert
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["title"], "Dashboard Meta")
        self.assertEqual(result[1]["title"], "Users Meta")
    
    @patch('app.application.services.menu_meta_service.MenuMeta')
    def test_update_menu_meta_success(self, mock_menu_meta_class):
        # Arrange
        menu_meta_id = "meta123"
        title = "Updated Dashboard Meta"
        icon = "updated-dashboard-icon"
        
        # Mock MenuMeta.objects.get to return a mock menu meta
        mock_menu_meta = Mock(spec=MenuMeta)
        mock_menu_meta.title = "Dashboard Meta"
        mock_menu_meta.icon = "dashboard-icon"
        mock_menu_meta.save.return_value = None
        
        mock_menu_meta_class.objects.get.return_value = mock_menu_meta
        
        # Act
        result = self.service.update_menu_meta(
            menu_meta_id=menu_meta_id,
            title=title,
            icon=icon
        )
        
        # Assert
        self.assertEqual(result["title"], title)
        self.assertEqual(result["icon"], icon)
        mock_menu_meta_class.objects.get.assert_called_once_with(id=menu_meta_id)
        mock_menu_meta.save.assert_called_once()
    
    @patch('app.application.services.menu_meta_service.MenuMeta')
    def test_delete_menu_meta_success(self, mock_menu_meta_class):
        # Arrange
        menu_meta_id = "meta123"
        
        # Mock MenuMeta.objects.get to return a mock menu meta
        mock_menu_meta = Mock(spec=MenuMeta)
        mock_menu_meta.delete.return_value = None
        
        mock_menu_meta_class.objects.get.return_value = mock_menu_meta
        
        # Act
        result = self.service.delete_menu_meta(menu_meta_id)
        
        # Assert
        self.assertTrue(result)
        mock_menu_meta_class.objects.get.assert_called_once_with(id=menu_meta_id)
        mock_menu_meta.delete.assert_called_once()
    
    @patch('app.application.services.menu_meta_service.MenuMeta')
    def test_get_menu_meta_not_found(self, mock_menu_meta_class):
        # Arrange
        menu_meta_id = "meta123"
        
        # Mock MenuMeta.objects.get to raise DoesNotExist
        mock_menu_meta_class.DoesNotExist = Exception
        mock_menu_meta_class.objects.get.side_effect = mock_menu_meta_class.DoesNotExist("MenuMeta does not exist")
        
        # Act & Assert
        with self.assertRaises(BusinessException):
            self.service.get_menu_meta(menu_meta_id)
    
    @patch('app.application.services.menu_meta_service.MenuMeta')
    def test_update_menu_meta_not_found(self, mock_menu_meta_class):
        # Arrange
        menu_meta_id = "meta123"
        title = "Updated Dashboard Meta"
        
        # Mock MenuMeta.objects.get to raise DoesNotExist
        mock_menu_meta_class.DoesNotExist = Exception
        mock_menu_meta_class.objects.get.side_effect = mock_menu_meta_class.DoesNotExist("MenuMeta does not exist")
        
        # Act & Assert
        with self.assertRaises(BusinessException):
            self.service.update_menu_meta(menu_meta_id=menu_meta_id, title=title)
    
    @patch('app.application.services.menu_meta_service.MenuMeta')
    def test_delete_menu_meta_not_found(self, mock_menu_meta_class):
        # Arrange
        menu_meta_id = "meta123"
        
        # Mock MenuMeta.objects.get to raise DoesNotExist
        mock_menu_meta_class.DoesNotExist = Exception
        mock_menu_meta_class.objects.get.side_effect = mock_menu_meta_class.DoesNotExist("MenuMeta does not exist")
        
        # Act & Assert
        with self.assertRaises(BusinessException):
            self.service.delete_menu_meta(menu_meta_id)