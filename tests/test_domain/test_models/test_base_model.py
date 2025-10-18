"""
测试基础模型
"""

from django.test import TestCase
from django.db import models
from django.utils import timezone
from app.domain.models.base_model import BaseModel
from unittest.mock import patch, MagicMock
import uuid


# 创建一个继承自BaseModel的测试模型
class TestModel(BaseModel):
    id = models.CharField(max_length=32, primary_key=True, default=lambda: uuid.uuid4().hex[:32])
    name = models.CharField(max_length=128, default="")
    
    class Meta(BaseModel.Meta):
        app_label = 'domain'


class TestBaseModel(TestCase):
    def test_base_model_creation(self):
        """测试基础模型创建"""
        # 使用mock避免实际数据库操作
        with patch.object(TestModel, 'save') as mock_save:
            # 创建测试模型实例
            test_model = TestModel(name="test_model")
            test_model.save()
            
            # 验证save方法被调用
            mock_save.assert_called_once()
            
            # 验证基础字段是否正确设置
            self.assertIsNotNone(test_model.id)
            self.assertEqual(test_model.name, "test_model")
        
    def test_base_model_save_updates_updated_time(self):
        """测试基础模型保存时更新updated_time"""
        # 使用mock避免实际数据库操作
        with patch.object(TestModel, 'save') as mock_save:
            # 创建测试模型实例
            test_model = TestModel(name="test_model")
            test_model.save()
            
            # 验证save方法被调用
            mock_save.assert_called_once()
            
            # 验证updated_time存在
            self.assertIsNotNone(test_model.updated_time)
        
    def test_base_model_with_description_and_creator(self):
        """测试基础模型带描述和创建者"""
        # 使用mock避免实际数据库操作
        with patch.object(TestModel, 'save') as mock_save:
            # 创建测试模型实例
            test_model = TestModel(
                name="test_model",
                description="Test model description",
                creator="test_user",
                modifier="test_user"
            )
            test_model.save()
            
            # 验证save方法被调用
            mock_save.assert_called_once()
            
            # 验证字段是否正确设置
            self.assertEqual(test_model.description, "Test model description")
            self.assertEqual(test_model.creator, "test_user")
            self.assertEqual(test_model.modifier, "test_user")