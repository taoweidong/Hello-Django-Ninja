"""
BaseModel测试用例
"""

from django.test import TestCase
from app.domain.models.base_model import BaseModel, set_current_user, get_current_user
from app.domain.models.department import Department


class TestBaseModel(TestCase):
    def setUp(self):
        """测试前准备"""
        pass

    def test_set_and_get_current_user(self):
        """测试设置和获取当前用户"""
        # 设置当前用户
        set_current_user("testuser")
        
        # 获取当前用户
        current_user = get_current_user()
        
        # 验证
        self.assertEqual(current_user, "testuser")

    def test_base_model_save_new_record(self):
        """测试保存新记录时自动设置创建时间和创建者"""
        # 设置当前用户
        set_current_user("testuser")
        
        # 创建新记录
        department = Department(
            name="Test Department",
            code="TEST001",
            rank=1,
            auto_bind=True,
            is_active=True,
            mode_type=1
        )
        department.save()
        
        # 验证创建时间和创建者已自动设置
        self.assertIsNotNone(department.created_time)
        # 修复测试：creator现在存储的是用户名字符串，而不是User对象
        self.assertEqual(department.creator, "testuser")
        self.assertEqual(department.modifier, "testuser")

    def test_base_model_save_existing_record(self):
        """测试更新记录时自动设置更新时间和修改者"""
        # 设置当前用户
        set_current_user("creator")
        
        # 创建新记录
        department = Department(
            name="Test Department",
            code="TEST002",
            rank=1,
            auto_bind=True,
            is_active=True,
            mode_type=1
        )
        department.save()
        
        # 记录创建时间
        original_created_time = department.created_time
        
        # 更改当前用户
        set_current_user("modifier")
        
        # 更新记录
        department.name = "Updated Department"
        department.save()
        
        # 验证创建时间未变，更新时间已更新，修改者已更新
        self.assertEqual(department.created_time, original_created_time)
        self.assertIsNotNone(department.updated_time)
        # 修复测试：creator现在存储的是用户名字符串，而不是User对象
        self.assertEqual(department.creator, "creator")
        self.assertEqual(department.modifier, "modifier")