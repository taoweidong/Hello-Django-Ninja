"""
测试部门模型
"""

from django.test import TestCase
from django.db import IntegrityError
from app.domain.models.department import Department
import uuid


class TestDepartmentModel(TestCase):
    def test_department_creation(self):
        """测试部门创建"""
        department_id = uuid.uuid4().hex[:32]
        department = Department(
            id=department_id,
            name="test_department",
            code="TEST_DEPT",
            rank=1,
            auto_bind=True,
            is_active=True,
            mode_type=0
        )
        department.save()
        
        self.assertEqual(department.id, department_id)
        self.assertEqual(department.name, "test_department")
        self.assertEqual(department.code, "TEST_DEPT")
        self.assertEqual(department.rank, 1)
        self.assertEqual(department.auto_bind, True)
        self.assertEqual(department.is_active, True)
        self.assertEqual(department.mode_type, 0)
        
    def test_department_str_representation(self):
        """测试部门字符串表示"""
        department = Department(
            id=uuid.uuid4().hex[:32],
            name="test_department",
            code="TEST_DEPT",
            rank=1,
            auto_bind=True,
            is_active=True,
            mode_type=0
        )
        department.save()
        
        self.assertEqual(str(department), "test_department")
        
    def test_department_unique_code(self):
        """测试部门code唯一性"""
        # 创建第一个部门
        department1 = Department(
            id=uuid.uuid4().hex[:32],
            name="department1",
            code="UNIQUE_CODE",
            rank=1,
            auto_bind=True,
            is_active=True,
            mode_type=0
        )
        department1.save()
        
        # 确保第一个部门已保存
        self.assertIsNotNone(department1.pk)
        
        # 尝试创建具有相同code的部门，应该抛出IntegrityError
        department2 = Department(
            id=uuid.uuid4().hex[:32],
            name="department2",
            code="UNIQUE_CODE",
            rank=2,
            auto_bind=False,
            is_active=False,
            mode_type=1
        )
        
        with self.assertRaises(IntegrityError):
            department2.save()
            
    def test_department_with_parent(self):
        """测试部门与父部门关系"""
        # 创建父部门
        parent_department = Department(
            id=uuid.uuid4().hex[:32],
            name="parent_department",
            code="PARENT_DEPT",
            rank=1,
            auto_bind=True,
            is_active=True,
            mode_type=0
        )
        parent_department.save()
        
        # 创建子部门
        child_department = Department(
            id=uuid.uuid4().hex[:32],
            name="child_department",
            code="CHILD_DEPT",
            rank=2,
            auto_bind=False,
            is_active=True,
            mode_type=0,
            parent=parent_department
        )
        child_department.save()
        
        # 验证父子关系
        self.assertEqual(child_department.parent, parent_department)
        self.assertIn(child_department, parent_department.children.all())