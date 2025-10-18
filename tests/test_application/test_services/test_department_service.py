"""
测试部门应用服务
"""

from django.test import TestCase
from app.application.services.department_service import DepartmentService
from app.domain.models.department import Department
from app.common.exception.exceptions import BusinessException
from unittest.mock import patch, MagicMock
import uuid
from django.core.exceptions import ObjectDoesNotExist


class TestDepartmentService(TestCase):
    def setUp(self):
        """测试初始化"""
        self.department_service = DepartmentService()

    def test_create_department_success(self):
        """测试成功创建部门"""
        # 准备测试数据
        department_data = {
            "name": "测试部门",
            "code": f"DEPT_{uuid.uuid4().hex[:8]}",
            "description": "测试部门描述",
            "rank": 1,
            "auto_bind": True,
            "is_active": True,
            "mode_type": 0,
            "parent_id": None
        }
        
        # 使用mock避免实际数据库操作
        with patch('app.domain.models.department.Department.save') as mock_save:
            with patch('app.domain.models.department.Department.objects.filter') as mock_filter:
                mock_filter.return_value.exists.return_value = False
                mock_department = MagicMock()
                mock_department.id = str(uuid.uuid4())
                mock_department.name = department_data["name"]
                mock_department.code = department_data["code"]
                mock_department.description = department_data["description"]
                mock_department.rank = department_data["rank"]
                mock_department.auto_bind = department_data["auto_bind"]
                mock_department.is_active = department_data["is_active"]
                mock_department.mode_type = department_data["mode_type"]
                mock_department.parent_id = department_data["parent_id"]
                mock_department.created_time = "2023-01-01T00:00:00Z"
                mock_department.updated_time = "2023-01-01T00:00:00Z"
                
                with patch('app.domain.models.department.Department', return_value=mock_department):
                    result = self.department_service.create_department(**department_data)
                    
                    # 验证结果
                    self.assertEqual(result["name"], department_data["name"])
                    self.assertEqual(result["code"], department_data["code"])
                    mock_save.assert_called_once()

    def test_create_department_duplicate_code(self):
        """测试创建部门时code重复"""
        department_data = {
            "name": "测试部门",
            "code": "DUPLICATE_CODE",
            "description": "测试部门描述",
            "rank": 0,
            "auto_bind": False,
            "is_active": True,
            "mode_type": 0
        }
        
        with patch('app.domain.models.department.Department.objects.filter') as mock_filter:
            mock_filter.return_value.exists.return_value = True
            
            with self.assertRaises(BusinessException) as context:
                self.department_service.create_department(**department_data)
            
            self.assertIn("already exists", str(context.exception))

    def test_get_department_success(self):
        """测试成功获取部门"""
        department_id = str(uuid.uuid4())
        mock_department = MagicMock()
        mock_department.id = department_id
        mock_department.name = "测试部门"
        mock_department.code = "TEST_DEPT"
        mock_department.description = "测试部门描述"
        mock_department.rank = 1
        mock_department.auto_bind = True
        mock_department.is_active = True
        mock_department.mode_type = 0
        mock_department.parent_id = None
        mock_department.created_time = "2023-01-01T00:00:00Z"
        mock_department.updated_time = "2023-01-01T00:00:00Z"
        
        with patch('app.domain.models.department.Department.objects.get', return_value=mock_department):
            result = self.department_service.get_department(department_id)
            
            self.assertEqual(result["id"], department_id)
            self.assertEqual(result["name"], "测试部门")

    def test_get_department_not_found(self):
        """测试获取不存在的部门"""
        department_id = str(uuid.uuid4())
        
        with patch('app.domain.models.department.Department.objects.get') as mock_get:
            # 创建一个模拟的Department.DoesNotExist异常
            class MockDoesNotExist(Exception):
                pass
            mock_get.side_effect = MockDoesNotExist()
            # 通过patch使Department.DoesNotExist指向我们的模拟异常
            with patch.object(Department, 'DoesNotExist', MockDoesNotExist):
                with self.assertRaises(BusinessException) as context:
                    self.department_service.get_department(department_id)
                
                self.assertIn("not found", str(context.exception))

    def test_update_department_success(self):
        """测试成功更新部门"""
        department_id = str(uuid.uuid4())
        mock_department = MagicMock()
        mock_department.id = department_id
        mock_department.name = "原始名称"
        mock_department.code = "ORIGINAL_CODE"
        mock_department.description = "原始描述"
        mock_department.rank = 1
        mock_department.auto_bind = True
        mock_department.is_active = True
        mock_department.mode_type = 0
        mock_department.parent_id = None
        mock_department.created_time = "2023-01-01T00:00:00Z"
        mock_department.updated_time = "2023-01-01T00:00:00Z"
        
        update_data = {
            "name": "更新后的名称",
            "code": "UPDATED_CODE",
            "rank": 2,
            "auto_bind": False,
            "is_active": False,
            "mode_type": 1
        }
        
        with patch('app.domain.models.department.Department.objects.get', return_value=mock_department):
            with patch('app.domain.models.department.Department.objects.filter') as mock_filter:
                mock_filter.return_value.exclude.return_value.exists.return_value = False
                result = self.department_service.update_department(department_id, **update_data)
                
                self.assertEqual(result["name"], update_data["name"])
                self.assertEqual(result["code"], update_data["code"])
                mock_department.save.assert_called_once()

    def test_update_department_not_found(self):
        """测试更新不存在的部门"""
        department_id = str(uuid.uuid4())
        
        with patch('app.domain.models.department.Department.objects.get') as mock_get:
            # 创建一个模拟的Department.DoesNotExist异常
            class MockDoesNotExist(Exception):
                pass
            mock_get.side_effect = MockDoesNotExist()
            # 通过patch使Department.DoesNotExist指向我们的模拟异常
            with patch.object(Department, 'DoesNotExist', MockDoesNotExist):
                with self.assertRaises(BusinessException) as context:
                    self.department_service.update_department(department_id, name="新名称")
                
                self.assertIn("not found", str(context.exception))

    def test_delete_department_success(self):
        """测试成功删除部门"""
        department_id = str(uuid.uuid4())
        mock_department = MagicMock()
        
        with patch('app.domain.models.department.Department.objects.get', return_value=mock_department):
            result = self.department_service.delete_department(department_id)
            
            self.assertTrue(result)
            mock_department.delete.assert_called_once()

    def test_delete_department_not_found(self):
        """测试删除不存在的部门"""
        department_id = str(uuid.uuid4())
        
        with patch('app.domain.models.department.Department.objects.get') as mock_get:
            # 创建一个模拟的Department.DoesNotExist异常
            class MockDoesNotExist(Exception):
                pass
            mock_get.side_effect = MockDoesNotExist()
            # 通过patch使Department.DoesNotExist指向我们的模拟异常
            with patch.object(Department, 'DoesNotExist', MockDoesNotExist):
                with self.assertRaises(BusinessException) as context:
                    self.department_service.delete_department(department_id)
                
                self.assertIn("not found", str(context.exception))

    def test_list_departments(self):
        """测试获取部门列表"""
        mock_departments = []
        for i in range(3):
            mock_dept = MagicMock()
            mock_dept.id = str(uuid.uuid4())
            mock_dept.name = f"部门{i}"
            mock_dept.code = f"DEPT_{i}"
            mock_dept.description = f"部门{i}描述"
            mock_dept.rank = i
            mock_dept.auto_bind = True
            mock_dept.is_active = True
            mock_dept.mode_type = 0
            mock_dept.parent_id = None
            mock_dept.created_time = "2023-01-01T00:00:00Z"
            mock_dept.updated_time = "2023-01-01T00:00:00Z"
            mock_departments.append(mock_dept)
        
        with patch('app.domain.models.department.Department.objects.all', return_value=mock_departments):
            result = self.department_service.list_departments()
            
            self.assertEqual(len(result), 3)
            self.assertEqual(result[0]["name"], "部门0")