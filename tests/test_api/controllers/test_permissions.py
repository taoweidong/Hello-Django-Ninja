# test_permissions_controller.py
from unittest.mock import Mock, patch
from django.test import TestCase
from app.application.services.permission_service import PermissionService
from app.domain.repositories.permission_repository import PermissionRepository
from django.contrib.auth.models import Permission as DjangoPermission
from django.contrib.contenttypes.models import ContentType
from app.common.exception.exceptions import BusinessException


class TestPermissionsController(TestCase):
    def setUp(self):
        self.permission_repo_mock = Mock(spec=PermissionRepository)
        self.service = PermissionService(self.permission_repo_mock)
    
    def test_create_permission_success(self):
        # Arrange
        name = "Can view users"
        codename = "view_users"
        
        # Mock ContentType
        mock_content_type = Mock(spec=ContentType)
        
        # Mock find_by_codename to return None (no existing permission with this codename)
        self.permission_repo_mock.find_by_codename.return_value = None
        
        # Create a mock permission object that will be passed to save
        mock_permission = Mock(spec=DjangoPermission)
        mock_permission.pk = 1
        mock_permission.name = name
        mock_permission.codename = codename
        
        # Mock the repository save method to just return None
        self.permission_repo_mock.save.return_value = None
        
        # We need to patch the Permission constructor to return our mock
        with patch.object(DjangoPermission, '__new__', return_value=mock_permission):
            # Act
            result = self.service.create_permission(name, codename, mock_content_type)
            
            # Assert
            self.assertEqual(result["name"], name)
            self.assertEqual(result["codename"], codename)
            self.permission_repo_mock.find_by_codename.assert_called_once_with(codename)
            self.permission_repo_mock.save.assert_called_once()
    
    def test_get_permission_success(self):
        # Arrange
        permission_id = 1
        name = "Can view users"
        codename = "view_users"
        
        # Create a mock permission object
        mock_permission = Mock(spec=DjangoPermission)
        mock_permission.pk = permission_id
        mock_permission.name = name
        mock_permission.codename = codename
        
        # Mock find_by_id to return the mock permission
        self.permission_repo_mock.find_by_id.return_value = mock_permission
        
        # Act
        result = self.service.get_permission_by_id(permission_id)
        
        # Assert
        self.assertEqual(result["name"], name)
        self.assertEqual(result["codename"], codename)
        self.permission_repo_mock.find_by_id.assert_called_once_with(permission_id)
    
    def test_list_permissions_success(self):
        # Arrange
        # Create mock permission objects
        mock_permission1 = Mock(spec=DjangoPermission)
        mock_permission1.pk = 1
        mock_permission1.name = "Can view users"
        mock_permission1.codename = "view_users"
        
        mock_permission2 = Mock(spec=DjangoPermission)
        mock_permission2.pk = 2
        mock_permission2.name = "Can edit users"
        mock_permission2.codename = "edit_users"
        
        # Mock list_all to return the mock permissions
        self.permission_repo_mock.list_all.return_value = [mock_permission1, mock_permission2]
        
        # Act
        result = self.service.list_permissions()
        
        # Assert
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["name"], "Can view users")
        self.assertEqual(result[1]["name"], "Can edit users")
        self.permission_repo_mock.list_all.assert_called_once()
    
    def test_update_permission_success(self):
        # Arrange
        permission_id = 1
        name = "Can view all users"
        codename = "view_all_users"
        
        # Mock ContentType
        mock_content_type = Mock(spec=ContentType)
        
        # Create a mock permission object
        mock_permission = Mock(spec=DjangoPermission)
        mock_permission.pk = permission_id
        mock_permission.name = "Can view users"
        mock_permission.codename = "view_users"
        
        # Mock find_by_id to return the mock permission
        self.permission_repo_mock.find_by_id.return_value = mock_permission
        
        # Mock the repository save method
        self.permission_repo_mock.save.return_value = None
        
        # Act
        result = self.service.update_permission(permission_id, name=name, codename=codename, content_type=mock_content_type)
        
        # Assert
        self.assertEqual(result["name"], name)
        self.assertEqual(result["codename"], codename)
        self.permission_repo_mock.find_by_id.assert_called_once_with(permission_id)
        self.permission_repo_mock.save.assert_called_once()
    
    def test_delete_permission_success(self):
        # Arrange
        permission_id = 1
        self.permission_repo_mock.delete.return_value = True
        
        # Act
        result = self.service.delete_permission(permission_id)
        
        # Assert
        self.assertTrue(result)
        self.permission_repo_mock.delete.assert_called_once_with(permission_id)
    
    def test_create_permission_codename_exists(self):
        # Arrange
        name = "Can view users"
        codename = "view_users"
        
        # Mock ContentType
        mock_content_type = Mock(spec=ContentType)
        
        # Mock find_by_codename to return an existing permission
        mock_existing_permission = Mock(spec=DjangoPermission)
        self.permission_repo_mock.find_by_codename.return_value = mock_existing_permission
        
        # Act & Assert
        with self.assertRaises(BusinessException):
            self.service.create_permission(name, codename, mock_content_type)
    
    def test_get_permission_not_found(self):
        # Arrange
        permission_id = 1
        self.permission_repo_mock.find_by_id.return_value = None
        
        # Act & Assert
        with self.assertRaises(BusinessException):
            self.service.get_permission_by_id(permission_id)
    
    def test_update_permission_not_found(self):
        # Arrange
        permission_id = 1
        name = "Can view all users"
        
        # Mock ContentType
        mock_content_type = Mock(spec=ContentType)
        
        self.permission_repo_mock.find_by_id.return_value = None
        
        # Act & Assert
        with self.assertRaises(BusinessException):
            self.service.update_permission(permission_id, name=name, content_type=mock_content_type)
    
    def test_delete_permission_not_found(self):
        # Arrange
        permission_id = 1
        self.permission_repo_mock.delete.return_value = False
        
        # Act & Assert
        with self.assertRaises(BusinessException):
            self.service.delete_permission(permission_id)