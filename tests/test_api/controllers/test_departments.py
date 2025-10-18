# test_departments_controller.py
from unittest.mock import Mock, patch
from django.test import TestCase
from app.application.services.department_service import DepartmentService
from app.domain.repositories.department_repository import DepartmentRepository
from app.domain.models.department import Department
from app.common.exception.exceptions import BusinessException
from datetime import datetime


class TestDepartmentsController(TestCase):
    def setUp(self):
        self.department_repo_mock = Mock(spec=DepartmentRepository)
        self.service = DepartmentService(self.department_repo_mock)
    
    def test_create_department_success(self):
        # Arrange
        name = "IT Department"
        code = "IT001"
        description = "Information Technology Department"
        rank = 1
        auto_bind = True
        is_active = True
        mode_type = 1  # 修复：使用整数而不是字符串
        parent_id = None
        
        # Mock find_by_code to return None (no existing department with this code)
        self.department_repo_mock.find_by_code.return_value = None
        
        # Create a mock department object
        mock_department = Mock(spec=Department)
        mock_department.id = "123e4567-e89b-12d3-a456-426614174000"
        mock_department.name = name
        mock_department.code = code
        mock_department.description = description
        mock_department.rank = rank
        mock_department.auto_bind = auto_bind
        mock_department.is_active = is_active
        mock_department.mode_type = mode_type
        mock_department.parent_id = parent_id
        mock_department.created_time = datetime.now()
        mock_department.updated_time = datetime.now()
        
        # Mock the _department_to_dict method result
        expected_response = {
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "name": "IT Department",
            "code": "IT001",
            "description": "Information Technology Department",
            "rank": 1,
            "auto_bind": True,
            "is_active": True,
            "mode_type": 1,
            "parent_id": None,
            "created_time": mock_department.created_time,
            "updated_time": mock_department.updated_time
        }
        
        # Act
        result = self.service.create_department(
            name=name,
            code=code,
            description=description,
            rank=rank,
            auto_bind=auto_bind,
            is_active=is_active,
            mode_type=mode_type,
            parent_id=parent_id
        )
        
        # Assert
        self.assertEqual(result["name"], expected_response["name"])
        self.assertEqual(result["code"], expected_response["code"])
        self.department_repo_mock.find_by_code.assert_called_once_with(code)
        self.department_repo_mock.save.assert_called_once()
    
    def test_get_department_success(self):
        # Arrange
        department_id = "123e4567-e89b-12d3-a456-426614174000"
        
        # Create a mock department object
        mock_department = Mock(spec=Department)
        mock_department.id = department_id
        mock_department.name = "IT Department"
        mock_department.code = "IT001"
        mock_department.description = "Information Technology Department"
        mock_department.rank = 1
        mock_department.auto_bind = True
        mock_department.is_active = True
        mock_department.mode_type = 1
        mock_department.parent_id = None
        mock_department.created_time = datetime.now()
        mock_department.updated_time = datetime.now()
        
        # Mock find_by_id to return the mock department
        self.department_repo_mock.find_by_id.return_value = mock_department
        
        # Mock the _department_to_dict method result
        expected_response = {
            "id": department_id,
            "name": "IT Department",
            "code": "IT001",
            "description": "Information Technology Department",
            "rank": 1,
            "auto_bind": True,
            "is_active": True,
            "mode_type": 1,
            "parent_id": None,
            "created_time": mock_department.created_time,
            "updated_time": mock_department.updated_time
        }
        
        # Act
        result = self.service.get_department(department_id)
        
        # Assert
        self.assertEqual(result["name"], expected_response["name"])
        self.assertEqual(result["code"], expected_response["code"])
        self.department_repo_mock.find_by_id.assert_called_once_with(department_id)
    
    def test_list_departments_success(self):
        # Arrange
        # Create mock department objects
        mock_department1 = Mock(spec=Department)
        mock_department1.id = "123e4567-e89b-12d3-a456-426614174000"
        mock_department1.name = "IT Department"
        mock_department1.code = "IT001"
        mock_department1.description = "Information Technology Department"
        mock_department1.rank = 1
        mock_department1.auto_bind = True
        mock_department1.is_active = True
        mock_department1.mode_type = 1
        mock_department1.parent_id = None
        mock_department1.created_time = datetime.now()
        mock_department1.updated_time = datetime.now()
        
        mock_department2 = Mock(spec=Department)
        mock_department2.id = "123e4567-e89b-12d3-a456-426614174001"
        mock_department2.name = "HR Department"
        mock_department2.code = "HR001"
        mock_department2.description = "Human Resources Department"
        mock_department2.rank = 2
        mock_department2.auto_bind = False
        mock_department2.is_active = True
        mock_department2.mode_type = 1
        mock_department2.parent_id = None
        mock_department2.created_time = datetime.now()
        mock_department2.updated_time = datetime.now()
        
        # Mock list_all to return the mock departments
        self.department_repo_mock.list_all.return_value = [mock_department1, mock_department2]
        
        # Act
        result = self.service.list_departments()
        
        # Assert
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["name"], "IT Department")
        self.assertEqual(result[1]["name"], "HR Department")
        self.department_repo_mock.list_all.assert_called_once()
    
    def test_update_department_success(self):
        # Arrange
        department_id = "123e4567-e89b-12d3-a456-426614174000"
        name = "Updated IT Department"
        code = "IT002"
        description = "Updated Information Technology Department"
        
        # Create a mock department object
        mock_department = Mock(spec=Department)
        mock_department.id = department_id
        mock_department.name = "IT Department"  # Original name
        mock_department.code = "IT001"  # Original code
        mock_department.description = "Information Technology Department"  # Original description
        mock_department.rank = 1
        mock_department.auto_bind = True
        mock_department.is_active = True
        mock_department.mode_type = 1
        mock_department.parent_id = None
        mock_department.created_time = datetime.now()
        mock_department.updated_time = datetime.now()
        
        # Mock find_by_id to return the mock department
        self.department_repo_mock.find_by_id.return_value = mock_department
        
        # Mock find_by_code to return None (no existing department with new code)
        self.department_repo_mock.find_by_code.return_value = None
        
        # Mock the _department_to_dict method result
        expected_response = {
            "id": department_id,
            "name": "Updated IT Department",
            "code": "IT002",
            "description": "Updated Information Technology Department",
            "rank": 1,
            "auto_bind": True,
            "is_active": True,
            "mode_type": 1,
            "parent_id": None,
            "created_time": mock_department.created_time,
            "updated_time": mock_department.updated_time
        }
        
        # Act
        result = self.service.update_department(
            department_id=department_id,
            name=name,
            code=code,
            description=description
        )
        
        # Assert
        self.assertEqual(result["name"], expected_response["name"])
        self.assertEqual(result["code"], expected_response["code"])
        self.department_repo_mock.find_by_id.assert_called_once_with(department_id)
        self.department_repo_mock.find_by_code.assert_called_once_with(code)
        self.department_repo_mock.save.assert_called_once()
    
    def test_delete_department_success(self):
        # Arrange
        department_id = "123e4567-e89b-12d3-a456-426614174000"
        self.department_repo_mock.delete.return_value = True
        
        # Act
        result = self.service.delete_department(department_id)
        
        # Assert
        self.assertTrue(result)
        self.department_repo_mock.delete.assert_called_once_with(department_id)
    
    def test_create_department_code_exists(self):
        # Arrange
        name = "IT Department"
        code = "IT001"
        description = "Information Technology Department"
        rank = 1
        auto_bind = True
        is_active = True
        mode_type = 1
        parent_id = None
        
        # Mock find_by_code to return an existing department
        mock_existing_department = Mock(spec=Department)
        self.department_repo_mock.find_by_code.return_value = mock_existing_department
        
        # Act & Assert
        with self.assertRaises(BusinessException):
            self.service.create_department(
                name=name,
                code=code,
                description=description,
                rank=rank,
                auto_bind=auto_bind,
                is_active=is_active,
                mode_type=mode_type,
                parent_id=parent_id
            )
    
    def test_get_department_not_found(self):
        # Arrange
        department_id = "123e4567-e89b-12d3-a456-426614174000"
        self.department_repo_mock.find_by_id.return_value = None
        
        # Act & Assert
        with self.assertRaises(BusinessException):
            self.service.get_department(department_id)
    
    def test_update_department_not_found(self):
        # Arrange
        department_id = "123e4567-e89b-12d3-a456-426614174000"
        name = "Updated Department"
        self.department_repo_mock.find_by_id.return_value = None
        
        # Act & Assert
        with self.assertRaises(BusinessException):
            self.service.update_department(
                department_id=department_id,
                name=name
            )
    
    def test_delete_department_not_found(self):
        # Arrange
        department_id = "123e4567-e89b-12d3-a456-426614174000"
        self.department_repo_mock.delete.return_value = False
        
        # Act & Assert
        with self.assertRaises(BusinessException):
            self.service.delete_department(department_id)