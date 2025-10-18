# test_roles_controller.py
from unittest.mock import Mock, patch
from django.test import TestCase
from app.application.services.role_service import RoleService
from app.domain.repositories.role_repository import RoleRepository
from app.domain.models.role import Role
from app.common.exception.exceptions import BusinessException


class TestRolesController(TestCase):
    def setUp(self):
        self.role_repo_mock = Mock(spec=RoleRepository)
        self.service = RoleService(self.role_repo_mock)
    
    def test_create_role_success(self):
        # Arrange
        name = "admin"
        description = "Administrator role"
        
        # Mock find_by_name to return None (no existing role with this name)
        self.role_repo_mock.find_by_name.return_value = None
        
        # Create a mock role object
        mock_role = Mock(spec=Role)
        mock_role.id = "123e4567-e89b-12d3-a456-426614174000"
        mock_role.name = name
        mock_role.description = description
        
        # Mock the repository save method
        self.role_repo_mock.save.return_value = None
        
        # Act
        result = self.service.create_role(name, description)
        
        # Assert
        self.assertEqual(result["name"], name)
        self.assertEqual(result["description"], description)
        self.role_repo_mock.find_by_name.assert_called_once_with(name)
        self.role_repo_mock.save.assert_called_once()
    
    def test_get_role_success(self):
        # Arrange
        role_id = "123e4567-e89b-12d3-a456-426614174000"
        name = "admin"
        description = "Administrator role"
        
        # Create a mock role object
        mock_role = Mock(spec=Role)
        mock_role.id = role_id
        mock_role.name = name
        mock_role.description = description
        
        # Mock find_by_id to return the mock role
        self.role_repo_mock.find_by_id.return_value = mock_role
        
        # Act
        result = self.service.get_role(role_id)
        
        # Assert
        self.assertEqual(result["name"], name)
        self.assertEqual(result["description"], description)
        self.role_repo_mock.find_by_id.assert_called_once_with(role_id)
    
    def test_list_roles_success(self):
        # Arrange
        # Create mock role objects
        mock_role1 = Mock(spec=Role)
        mock_role1.id = "123e4567-e89b-12d3-a456-426614174000"
        mock_role1.name = "admin"
        mock_role1.description = "Administrator role"
        
        mock_role2 = Mock(spec=Role)
        mock_role2.id = "123e4567-e89b-12d3-a456-426614174001"
        mock_role2.name = "user"
        mock_role2.description = "Regular user role"
        
        # Mock list_all to return the mock roles
        self.role_repo_mock.list_all.return_value = [mock_role1, mock_role2]
        
        # Act
        result = self.service.list_roles()
        
        # Assert
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["name"], "admin")
        self.assertEqual(result[1]["name"], "user")
        self.role_repo_mock.list_all.assert_called_once()
    
    def test_update_role_success(self):
        # Arrange
        role_id = "123e4567-e89b-12d3-a456-426614174000"
        name = "updated_admin"
        description = "Updated administrator role"
        
        # Create a mock role object
        mock_role = Mock(spec=Role)
        mock_role.id = role_id
        mock_role.name = "admin"
        mock_role.description = "Administrator role"
        
        # Mock find_by_id to return the mock role
        self.role_repo_mock.find_by_id.return_value = mock_role
        
        # Mock the repository save method
        self.role_repo_mock.save.return_value = None
        
        # Act
        result = self.service.update_role(role_id, name=name, description=description)
        
        # Assert
        self.assertEqual(result["name"], name)
        self.assertEqual(result["description"], description)
        self.role_repo_mock.find_by_id.assert_called_once_with(role_id)
        self.role_repo_mock.save.assert_called_once()
    
    def test_delete_role_success(self):
        # Arrange
        role_id = "123e4567-e89b-12d3-a456-426614174000"
        self.role_repo_mock.delete.return_value = True
        
        # Act
        result = self.service.delete_role(role_id)
        
        # Assert
        self.assertTrue(result)
        self.role_repo_mock.delete.assert_called_once_with(role_id)
    
    def test_create_role_name_exists(self):
        # Arrange
        name = "admin"
        description = "Administrator role"
        
        # Mock find_by_name to return an existing role
        mock_existing_role = Mock(spec=Role)
        self.role_repo_mock.find_by_name.return_value = mock_existing_role
        
        # Act & Assert
        with self.assertRaises(BusinessException):
            self.service.create_role(name, description)
    
    def test_get_role_not_found(self):
        # Arrange
        role_id = "123e4567-e89b-12d3-a456-426614174000"
        self.role_repo_mock.find_by_id.return_value = None
        
        # Act & Assert
        with self.assertRaises(BusinessException):
            self.service.get_role(role_id)
    
    def test_update_role_not_found(self):
        # Arrange
        role_id = "123e4567-e89b-12d3-a456-426614174000"
        name = "updated_admin"
        self.role_repo_mock.find_by_id.return_value = None
        
        # Act & Assert
        with self.assertRaises(BusinessException):
            self.service.update_role(role_id, name=name)
    
    def test_delete_role_not_found(self):
        # Arrange
        role_id = "123e4567-e89b-12d3-a456-426614174000"
        self.role_repo_mock.delete.return_value = False
        
        # Act & Assert
        with self.assertRaises(BusinessException):
            self.service.delete_role(role_id)