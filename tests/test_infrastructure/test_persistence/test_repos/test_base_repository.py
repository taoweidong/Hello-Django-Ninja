"""
测试基础仓储类
"""

from django.test import TestCase
from django.db import models
from app.infrastructure.persistence.repos.base_repository import BaseRepository
from unittest.mock import patch, MagicMock
import uuid


class TestBaseRepository(TestCase):
    def setUp(self):
        """测试初始化"""
        # 创建一个测试模型类，使用唯一的app_label避免冲突
        class TestModel(models.Model):
            id = models.CharField(max_length=32, primary_key=True)
            name = models.CharField(max_length=128)
            
            class Meta:
                app_label = f'test_{uuid.uuid4().hex[:8]}'  # 使用唯一标识避免冲突
        
        self.TestModel = TestModel
        self.repository = BaseRepository(TestModel)
        
    def test_base_repository_initialization(self):
        """测试基础仓储初始化"""
        self.assertEqual(self.repository.model_class, self.TestModel)
        
    def test_base_repository_save(self):
        """测试基础仓储保存实体"""
        # 创建测试实体
        entity = self.TestModel(id=uuid.uuid4().hex[:32], name="test_entity")
        
        # 使用mock避免实际数据库操作
        with patch.object(entity, 'save') as mock_save:
            self.repository.save(entity)
            mock_save.assert_called_once()
            
    def test_base_repository_list_all(self):
        """测试基础仓储获取所有实体列表"""
        mock_entities = [MagicMock(), MagicMock(), MagicMock()]
        
        # 使用对象本身进行mock
        # type: ignore
        with patch.object(self.TestModel.objects, 'all', return_value=mock_entities) as mock_all:
            result = self.repository.list_all()
            mock_all.assert_called_once()
            self.assertEqual(result, mock_entities)