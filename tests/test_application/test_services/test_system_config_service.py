"""
测试系统配置应用服务
"""

from django.test import TestCase
from app.application.services.system_config_service import SystemConfigService
from app.domain.models.system_config import SystemConfig
from app.common.exception.exceptions import BusinessException
from unittest.mock import Mock, patch
import uuid


class TestSystemConfigService(TestCase):
    def setUp(self):
        """测试初始化"""
        self.system_config_service = SystemConfigService()

    def test_create_system_config_success(self):
        """测试成功创建系统配置"""
        # 准备测试数据
        config_data = {
            "key": "test_key",
            "value": "test_value",
            "is_active": True,
            "access": True,
            "inherit": True,
            "description": "测试配置"
        }
        
        # 创建mock的system_config对象
        mock_config = Mock(spec=SystemConfig)
        mock_config.id = str(uuid.uuid4())
        mock_config.key = config_data["key"]
        mock_config.value = config_data["value"]
        mock_config.is_active = config_data["is_active"]
        mock_config.access = config_data["access"]
        mock_config.inherit = config_data["inherit"]
        mock_config.description = config_data["description"]
        mock_config.created_time = "2023-01-01T00:00:00Z"
        mock_config.updated_time = "2023-01-01T00:00:00Z"
        
        # 设置mock行为
        with patch('app.application.services.system_config_service.SystemConfig') as mock_config_class:
            # 模拟key不存在
            mock_config_class.objects.filter.return_value.exists.return_value = False
            mock_config_class.return_value = mock_config
            mock_config.save.return_value = None
            
            result = self.system_config_service.create_system_config(**config_data)
            
            # 验证结果
            self.assertEqual(result["key"], config_data["key"])
            self.assertEqual(result["value"], config_data["value"])
            self.assertEqual(result["description"], config_data["description"])

    def test_create_system_config_duplicate_key(self):
        """测试创建系统配置时key重复"""
        config_data = {
            "key": "duplicate_key",
            "value": "test_value",
            "is_active": True,
            "access": True,
            "inherit": True,
            "description": "测试配置"
        }
        
        # 设置mock行为，模拟key已存在
        with patch('app.application.services.system_config_service.SystemConfig') as mock_config_class:
            mock_config_class.objects.filter.return_value.exists.return_value = True
            
            with self.assertRaises(BusinessException) as context:
                self.system_config_service.create_system_config(**config_data)
            
            self.assertIn("already exists", str(context.exception))

    def test_get_system_config_success(self):
        """测试成功获取系统配置"""
        config_id = str(uuid.uuid4())
        mock_config = Mock(spec=SystemConfig)
        mock_config.id = config_id
        mock_config.key = "test_key"
        mock_config.value = "test_value"
        mock_config.is_active = True
        mock_config.access = True
        mock_config.inherit = True
        mock_config.description = "测试配置"
        mock_config.created_time = "2023-01-01T00:00:00Z"
        mock_config.updated_time = "2023-01-01T00:00:00Z"
        
        # 设置mock行为
        with patch('app.application.services.system_config_service.SystemConfig.objects.get') as mock_get:
            mock_get.return_value = mock_config
            
            result = self.system_config_service.get_system_config(config_id)
            
            self.assertEqual(result["id"], config_id)
            self.assertEqual(result["key"], "test_key")
            mock_get.assert_called_once_with(id=config_id)

    def test_get_system_config_not_found(self):
        """测试获取不存在的系统配置"""
        config_id = str(uuid.uuid4())
        
        # 设置mock行为，模拟配置不存在
        with patch('app.application.services.system_config_service.SystemConfig.objects.get') as mock_get:
            mock_get.side_effect = SystemConfig.DoesNotExist
            
            with self.assertRaises(BusinessException) as context:
                self.system_config_service.get_system_config(config_id)
            
            self.assertIn("not found", str(context.exception))

    def test_get_system_config_by_key_success(self):
        """测试根据key成功获取系统配置"""
        key = "test_key"
        mock_config = Mock(spec=SystemConfig)
        mock_config.id = str(uuid.uuid4())
        mock_config.key = key
        mock_config.value = "test_value"
        mock_config.is_active = True
        mock_config.access = True
        mock_config.inherit = True
        mock_config.description = "测试配置"
        mock_config.created_time = "2023-01-01T00:00:00Z"
        mock_config.updated_time = "2023-01-01T00:00:00Z"
        
        # 设置mock行为
        with patch('app.application.services.system_config_service.SystemConfig.objects.get') as mock_get:
            mock_get.return_value = mock_config
            
            result = self.system_config_service.get_system_config_by_key(key)
            
            self.assertEqual(result["key"], key)
            self.assertEqual(result["value"], "test_value")
            mock_get.assert_called_once_with(key=key)

    def test_get_system_config_by_key_not_found(self):
        """测试根据key获取不存在的系统配置"""
        key = "nonexistent_key"
        
        # 设置mock行为，模拟配置不存在
        with patch('app.application.services.system_config_service.SystemConfig.objects.get') as mock_get:
            mock_get.side_effect = SystemConfig.DoesNotExist
            
            with self.assertRaises(BusinessException) as context:
                self.system_config_service.get_system_config_by_key(key)
            
            self.assertIn("not found", str(context.exception))

    def test_update_system_config_success(self):
        """测试成功更新系统配置"""
        config_id = str(uuid.uuid4())
        mock_config = Mock(spec=SystemConfig)
        mock_config.id = config_id
        mock_config.key = "original_key"
        mock_config.value = "original_value"
        mock_config.is_active = True
        mock_config.access = True
        mock_config.inherit = True
        mock_config.description = "原始配置"
        mock_config.created_time = "2023-01-01T00:00:00Z"
        mock_config.updated_time = "2023-01-01T00:00:00Z"
        mock_config.save.return_value = None
        
        update_data = {
            "key": "updated_key",
            "value": "updated_value",
            "is_active": False,
            "access": False,
            "inherit": False,
            "description": "更新配置"
        }
        
        # 设置mock行为
        with patch('app.application.services.system_config_service.SystemConfig.objects.get') as mock_get:
            with patch('app.application.services.system_config_service.SystemConfig') as mock_config_class:
                # 模拟新key不存在（排除当前配置）
                mock_config_class.objects.filter.return_value.exclude.return_value.exists.return_value = False
                mock_get.return_value = mock_config
                
                result = self.system_config_service.update_system_config(config_id, **update_data)
                
                self.assertEqual(result["key"], update_data["key"])
                self.assertEqual(result["value"], update_data["value"])
                self.assertEqual(result["description"], update_data["description"])

    def test_update_system_config_not_found(self):
        """测试更新不存在的系统配置"""
        config_id = str(uuid.uuid4())
        
        # 设置mock行为，模拟配置不存在
        with patch('app.application.services.system_config_service.SystemConfig.objects.get') as mock_get:
            mock_get.side_effect = SystemConfig.DoesNotExist
            
            with self.assertRaises(BusinessException) as context:
                self.system_config_service.update_system_config(config_id, key="new_key")
            
            self.assertIn("not found", str(context.exception))

    def test_update_system_config_duplicate_key(self):
        """测试更新系统配置时key重复"""
        config_id = str(uuid.uuid4())
        
        # 设置mock行为，模拟key已存在（排除当前配置）
        with patch('app.application.services.system_config_service.SystemConfig.objects.get') as mock_get:
            with patch('app.application.services.system_config_service.SystemConfig') as mock_config_class:
                mock_config_class.objects.filter.return_value.exclude.return_value.exists.return_value = True
                mock_get.return_value = Mock(spec=SystemConfig)
                
                with self.assertRaises(BusinessException) as context:
                    self.system_config_service.update_system_config(config_id, key="duplicate_key")
                
                self.assertIn("already exists", str(context.exception))

    def test_delete_system_config_success(self):
        """测试成功删除系统配置"""
        config_id = str(uuid.uuid4())
        mock_config = Mock(spec=SystemConfig)
        mock_config.delete.return_value = None
        
        # 设置mock行为
        with patch('app.application.services.system_config_service.SystemConfig.objects.get') as mock_get:
            mock_get.return_value = mock_config
            
            result = self.system_config_service.delete_system_config(config_id)
            
            self.assertTrue(result)
            mock_config.delete.assert_called_once()

    def test_delete_system_config_not_found(self):
        """测试删除不存在的系统配置"""
        config_id = str(uuid.uuid4())
        
        # 设置mock行为，模拟配置不存在
        with patch('app.application.services.system_config_service.SystemConfig.objects.get') as mock_get:
            mock_get.side_effect = SystemConfig.DoesNotExist
            
            with self.assertRaises(BusinessException) as context:
                self.system_config_service.delete_system_config(config_id)
            
            self.assertIn("not found", str(context.exception))

    def test_list_system_configs(self):
        """测试获取系统配置列表"""
        mock_configs = []
        for i in range(3):
            mock_config = Mock(spec=SystemConfig)
            mock_config.id = str(uuid.uuid4())
            mock_config.key = f"key_{i}"
            mock_config.value = f"value_{i}"
            mock_config.is_active = i % 2 == 0
            mock_config.access = i % 2 == 0
            mock_config.inherit = i % 2 == 0
            mock_config.description = f"配置{i}"
            mock_config.created_time = "2023-01-01T00:00:00Z"
            mock_config.updated_time = "2023-01-01T00:00:00Z"
            mock_configs.append(mock_config)
        
        # 设置mock行为
        with patch('app.application.services.system_config_service.SystemConfig.objects.all') as mock_all:
            mock_all.return_value = mock_configs
            
            result = self.system_config_service.list_system_configs()
            
            self.assertEqual(len(result), 3)
            self.assertEqual(result[0]["key"], "key_0")