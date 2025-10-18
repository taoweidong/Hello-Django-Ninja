# test_system_configs_controller.py
from unittest.mock import Mock, patch
from django.test import TestCase
from app.application.services.system_config_service import SystemConfigService
from app.domain.models.system_config import SystemConfig
from app.common.exception.exceptions import BusinessException
from datetime import datetime


class TestSystemConfigsController(TestCase):
    def setUp(self):
        self.service = SystemConfigService()
    
    def test_create_system_config_success(self):
        # Arrange
        key = "app_name"
        value = "MyApp"
        is_active = True
        access = True
        inherit = True
        description = "Application name"
        
        # Mock SystemConfig.objects.filter to return empty queryset (no existing config with this key)
        mock_queryset = Mock()
        mock_queryset.exists.return_value = False
        with patch('app.domain.models.system_config.SystemConfig.objects.filter', return_value=mock_queryset):
            # Mock SystemConfig constructor and save method
            with patch('app.domain.models.system_config.SystemConfig') as MockSystemConfig:
                mock_config_instance = Mock(spec=SystemConfig)
                mock_config_instance.id = "config123"
                mock_config_instance.key = key
                mock_config_instance.value = value
                mock_config_instance.is_active = is_active
                mock_config_instance.access = access
                mock_config_instance.inherit = inherit
                mock_config_instance.description = description
                mock_config_instance.created_time = datetime.now()
                mock_config_instance.updated_time = datetime.now()
                
                MockSystemConfig.return_value = mock_config_instance
                mock_config_instance.save.return_value = None
                
                # Act
                result = self.service.create_system_config(
                    key=key,
                    value=value,
                    is_active=is_active,
                    access=access,
                    inherit=inherit,
                    description=description
                )
                
                # Assert
                self.assertEqual(result["key"], key)
                self.assertEqual(result["value"], value)
                MockSystemConfig.assert_called_once_with(
                    key=key,
                    value=value,
                    is_active=is_active,
                    access=access,
                    inherit=inherit,
                    description=description
                )
                mock_config_instance.save.assert_called_once()
    
    def test_get_system_config_success(self):
        # Arrange
        config_id = "config123"
        key = "app_name"
        value = "MyApp"
        is_active = True
        access = True
        inherit = True
        description = "Application name"
        
        # Mock SystemConfig.objects.get to return a mock config
        with patch('app.domain.models.system_config.SystemConfig.objects.get') as mock_config_get:
            mock_config = Mock(spec=SystemConfig)
            mock_config.id = config_id
            mock_config.key = key
            mock_config.value = value
            mock_config.is_active = is_active
            mock_config.access = access
            mock_config.inherit = inherit
            mock_config.description = description
            mock_config.created_time = datetime.now()
            mock_config.updated_time = datetime.now()
            
            mock_config_get.return_value = mock_config
            
            # Act
            result = self.service.get_system_config(config_id)
            
            # Assert
            self.assertEqual(result["key"], key)
            self.assertEqual(result["value"], value)
            mock_config_get.assert_called_once_with(id=config_id)
    
    def test_list_system_configs_success(self):
        # Arrange
        # Create mock config objects
        mock_config1 = Mock(spec=SystemConfig)
        mock_config1.id = "config123"
        mock_config1.key = "app_name"
        mock_config1.value = "MyApp"
        mock_config1.is_active = True
        mock_config1.access = True
        mock_config1.inherit = True
        mock_config1.description = "Application name"
        mock_config1.created_time = datetime.now()
        mock_config1.updated_time = datetime.now()
        
        mock_config2 = Mock(spec=SystemConfig)
        mock_config2.id = "config456"
        mock_config2.key = "app_version"
        mock_config2.value = "1.0.0"
        mock_config2.is_active = True
        mock_config2.access = True
        mock_config2.inherit = True
        mock_config2.description = "Application version"
        mock_config2.created_time = datetime.now()
        mock_config2.updated_time = datetime.now()
        
        # Mock SystemConfig.objects.all to return the mock configs
        with patch('app.domain.models.system_config.SystemConfig.objects.all', return_value=[mock_config1, mock_config2]):
            # Act
            result = self.service.list_system_configs()
            
            # Assert
            self.assertEqual(len(result), 2)
            self.assertEqual(result[0]["key"], "app_name")
            self.assertEqual(result[1]["key"], "app_version")
    
    def test_update_system_config_success(self):
        # Arrange
        config_id = "config123"
        key = "updated_app_name"
        value = "UpdatedApp"
        
        # Mock SystemConfig.objects.get to return a mock config
        with patch('app.domain.models.system_config.SystemConfig.objects.get') as mock_config_get:
            mock_config = Mock(spec=SystemConfig)
            mock_config.key = "app_name"
            mock_config.value = "MyApp"
            
            mock_config_get.return_value = mock_config
            
            # Mock SystemConfig.objects.filter to return empty queryset (no existing config with new key)
            mock_queryset = Mock()
            mock_queryset.exists.return_value = False
            mock_queryset.exclude.return_value = mock_queryset
            with patch('app.domain.models.system_config.SystemConfig.objects.filter', return_value=mock_queryset):
                mock_config.save.return_value = None
                
                # Act
                result = self.service.update_system_config(
                    config_id=config_id,
                    key=key,
                    value=value
                )
                
                # Assert
                self.assertEqual(result["key"], key)
                self.assertEqual(result["value"], value)
                mock_config_get.assert_called_once_with(id=config_id)
                mock_config.save.assert_called_once()
    
    def test_delete_system_config_success(self):
        # Arrange
        config_id = "config123"
        
        # Mock SystemConfig.objects.get to return a mock config
        with patch('app.domain.models.system_config.SystemConfig.objects.get') as mock_config_get:
            mock_config = Mock(spec=SystemConfig)
            mock_config.delete.return_value = None
            
            mock_config_get.return_value = mock_config
            
            # Act
            result = self.service.delete_system_config(config_id)
            
            # Assert
            self.assertTrue(result)
            mock_config_get.assert_called_once_with(id=config_id)
            mock_config.delete.assert_called_once()
    
    def test_create_system_config_key_exists(self):
        # Arrange
        key = "app_name"
        value = "MyApp"
        is_active = True
        access = True
        inherit = True
        
        # Mock SystemConfig.objects.filter to return queryset that exists (config with this key already exists)
        mock_queryset = Mock()
        mock_queryset.exists.return_value = True
        with patch('app.domain.models.system_config.SystemConfig.objects.filter', return_value=mock_queryset):
            # Act & Assert
            with self.assertRaises(BusinessException):
                self.service.create_system_config(
                    key=key,
                    value=value,
                    is_active=is_active,
                    access=access,
                    inherit=inherit
                )
    
    def test_get_system_config_not_found(self):
        # Arrange
        config_id = "config123"
        
        # Mock SystemConfig.objects.get to raise DoesNotExist
        with patch('app.domain.models.system_config.SystemConfig.objects.get') as mock_config_get:
            # 创建一个DoesNotExist异常实例
            does_not_exist_exception = Exception("SystemConfig does not exist")
            mock_config_get.side_effect = does_not_exist_exception
            
            # Act & Assert
            with self.assertRaises(BusinessException):
                self.service.get_system_config(config_id)
    
    def test_update_system_config_not_found(self):
        # Arrange
        config_id = "config123"
        key = "updated_app_name"
        
        # Mock SystemConfig.objects.get to raise DoesNotExist
        with patch('app.domain.models.system_config.SystemConfig.objects.get') as mock_config_get:
            # 创建一个DoesNotExist异常实例
            does_not_exist_exception = Exception("SystemConfig does not exist")
            mock_config_get.side_effect = does_not_exist_exception
            
            # Act & Assert
            with self.assertRaises(BusinessException):
                self.service.update_system_config(config_id=config_id, key=key)
    
    def test_delete_system_config_not_found(self):
        # Arrange
        config_id = "config123"
        
        # Mock SystemConfig.objects.get to raise DoesNotExist
        with patch('app.domain.models.system_config.SystemConfig.objects.get') as mock_config_get:
            # 创建一个DoesNotExist异常实例
            does_not_exist_exception = Exception("SystemConfig does not exist")
            mock_config_get.side_effect = does_not_exist_exception
            
            # Act & Assert
            with self.assertRaises(BusinessException):
                self.service.delete_system_config(config_id)