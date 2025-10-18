# test_users_controller.py
from unittest.mock import Mock, patch
from django.test import TestCase
from app.application.services.user_service import UserService
from app.domain.repositories.user_repository import UserRepository
from app.domain.models.user import User
from app.common.exception.exceptions import BusinessException


class TestUsersController(TestCase):
    def setUp(self):
        self.user_repo_mock = Mock(spec=UserRepository)
        self.service = UserService(self.user_repo_mock)
    
    def test_create_user_success(self):
        # Arrange
        username = "testuser"
        email = "test@example.com"
        password = "testpassword"
        
        # Mock find_by_username to return None (no existing user with this username)
        self.user_repo_mock.find_by_username.return_value = None
        
        # Create a mock user object
        mock_user = Mock(spec=User)
        mock_user.id = 1
        mock_user.username = username
        mock_user.email = email
        
        # Mock the repository save method
        self.user_repo_mock.save.return_value = None
        
        # Act
        result = self.service.create_user(username, email, password)
        
        # Assert
        self.assertEqual(result["username"], username)
        self.assertEqual(result["email"], email)
        self.user_repo_mock.find_by_username.assert_called_once_with(username)
        self.user_repo_mock.save.assert_called_once()
    
    def test_get_user_success(self):
        # Arrange
        user_id = 1
        username = "testuser"
        email = "test@example.com"
        
        # Create a mock user object
        mock_user = Mock(spec=User)
        mock_user.id = user_id
        mock_user.username = username
        mock_user.email = email
        
        # Mock find_by_id to return the mock user
        self.user_repo_mock.find_by_id.return_value = mock_user
        
        # Act
        result = self.service.get_user(user_id)
        
        # Assert
        self.assertEqual(result["username"], username)
        self.assertEqual(result["email"], email)
        self.user_repo_mock.find_by_id.assert_called_once_with(user_id)
    
    def test_list_users_success(self):
        # Arrange
        # Create mock user objects
        mock_user1 = Mock(spec=User)
        mock_user1.id = 1
        mock_user1.username = "user1"
        mock_user1.email = "user1@example.com"
        
        mock_user2 = Mock(spec=User)
        mock_user2.id = 2
        mock_user2.username = "user2"
        mock_user2.email = "user2@example.com"
        
        # Mock list_all to return the mock users
        self.user_repo_mock.list_all.return_value = [mock_user1, mock_user2]
        
        # Act
        result = self.service.list_users()
        
        # Assert
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["username"], "user1")
        self.assertEqual(result[1]["username"], "user2")
        self.user_repo_mock.list_all.assert_called_once()
    
    def test_update_user_success(self):
        # Arrange
        user_id = 1
        username = "updateduser"
        email = "updated@example.com"
        
        # Create a mock user object
        mock_user = Mock(spec=User)
        mock_user.id = user_id
        mock_user.username = "originaluser"
        mock_user.email = "original@example.com"
        
        # Mock find_by_id to return the mock user
        self.user_repo_mock.find_by_id.return_value = mock_user
        
        # Mock the repository save method
        self.user_repo_mock.save.return_value = None
        
        # Act
        result = self.service.update_user(user_id, username=username, email=email)
        
        # Assert
        self.assertEqual(result["username"], username)
        self.assertEqual(result["email"], email)
        self.user_repo_mock.find_by_id.assert_called_once_with(user_id)
        self.user_repo_mock.save.assert_called_once()
    
    def test_delete_user_success(self):
        # Arrange
        user_id = 1
        self.user_repo_mock.delete.return_value = True
        
        # Act
        result = self.service.delete_user(user_id)
        
        # Assert
        self.assertTrue(result)
        self.user_repo_mock.delete.assert_called_once_with(user_id)
    
    def test_create_user_username_exists(self):
        # Arrange
        username = "testuser"
        email = "test@example.com"
        password = "testpassword"
        
        # Mock find_by_username to return an existing user
        mock_existing_user = Mock(spec=User)
        self.user_repo_mock.find_by_username.return_value = mock_existing_user
        
        # Act & Assert
        with self.assertRaises(BusinessException):
            self.service.create_user(username, email, password)
    
    def test_get_user_not_found(self):
        # Arrange
        user_id = 1
        self.user_repo_mock.find_by_id.return_value = None
        
        # Act & Assert
        with self.assertRaises(BusinessException):
            self.service.get_user(user_id)
    
    def test_update_user_not_found(self):
        # Arrange
        user_id = 1
        username = "updateduser"
        self.user_repo_mock.find_by_id.return_value = None
        
        # Act & Assert
        with self.assertRaises(BusinessException):
            self.service.update_user(user_id, username=username)
    
    def test_delete_user_not_found(self):
        # Arrange
        user_id = 1
        self.user_repo_mock.delete.return_value = False
        
        # Act & Assert
        with self.assertRaises(BusinessException):
            self.service.delete_user(user_id)