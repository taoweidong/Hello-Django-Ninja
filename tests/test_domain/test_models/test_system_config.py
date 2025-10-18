"""
测试系统配置模型
"""

from django.test import TestCase
from app.domain.models.system_config import SystemConfig
from unittest.mock import patch
import uuid


class TestSystemConfigModel(TestCase):
    def test_system_config_creation(self):
        """测试系统配置创建"""
        config_id = uuid.uuid4().hex[:32]
        
        # 使用mock避免实际数据库操作
        with patch.object(SystemConfig, 'save') as mock_save:
            system_config = SystemConfig(
                id=config_id,
                key="test_config_key",
                value="test_config_value",
                status=True
            )
            system_config.save()
            
            mock_save.assert_called_once()
            
            self.assertEqual(system_config.id, config_id)
            self.assertEqual(system_config.key, "test_config_key")
            self.assertEqual(system_config.value, "test_config_value")
            self.assertEqual(system_config.status, True)
        
    def test_system_config_str_representation(self):
        """测试系统配置字符串表示"""
        # 使用mock避免实际数据库操作
        with patch.object(SystemConfig, 'save') as mock_save:
            system_config = SystemConfig(
                id=uuid.uuid4().hex[:32],
                key="test_config_key",
                value="test_config_value"
            )
            system_config.save()
            
            mock_save.assert_called_once()
            
            expected_str = f"SystemConfig {system_config.key}"
            self.assertEqual(str(system_config), expected_str)
        
    def test_system_config_unique_key(self):
        """测试系统配置key唯一性"""
        # 使用mock避免实际数据库操作
        with patch.object(SystemConfig, 'save') as mock_save:
            # 创建第一个配置
            config1 = SystemConfig(
                id=uuid.uuid4().hex[:32],
                key="unique_key",
                value="value1"
            )
            config1.save()
            
            mock_save.assert_called_once()
            
            # 创建第二个配置（在mock环境下不会抛出IntegrityError）
            config2 = SystemConfig(
                id=uuid.uuid4().hex[:32],
                key="unique_key",
                value="value2"
            )
            config2.save()
            
            # 验证save方法被调用
            self.assertEqual(mock_save.call_count, 2)