# test_login_logs_controller.py
from unittest.mock import Mock, patch
from django.test import TestCase
from app.application.services.login_log_service import LoginLogService
from app.domain.repositories.login_log_repository import LoginLogRepository
from app.domain.repositories.user_repository import UserRepository
from app.domain.models.login_log import LoginLog
from app.domain.models.user import User
from app.common.exception.exceptions import BusinessException
from datetime import datetime


class TestLoginLogsController(TestCase):
    def setUp(self):
        self.login_log_repo_mock = Mock(spec=LoginLogRepository)
        self.user_repo_mock = Mock(spec=UserRepository)
        self.service = LoginLogService(self.login_log_repo_mock, self.user_repo_mock)
    
    @patch('app.application.services.login_log_service.LoginLog')
    def test_create_login_log_success(self, mock_login_log_class):
        # Arrange
        status = True
        login_type = 1
        ipaddress = "192.168.1.1"
        browser = "Chrome"
        system = "Windows"
        agent = "Mozilla/5.0"
        creator_id = 1
        
        # Mock user_repo.find_by_id to return a mock user
        mock_user = Mock(spec=User)
        mock_user.id = creator_id
        self.user_repo_mock.find_by_id.return_value = mock_user
        
        # Create a mock login log object
        mock_log = Mock(spec=LoginLog)
        mock_log.id = 1
        mock_log.status = status
        mock_log.login_type = login_type
        mock_log.ipaddress = ipaddress
        mock_log.browser = browser
        mock_log.system = system
        mock_log.agent = agent
        mock_log.creator = mock_user
        mock_log.created_time = datetime.now()
        mock_log.updated_time = datetime.now()
        
        # Mock the LoginLog class to return our mock log when instantiated
        mock_login_log_class.return_value = mock_log
        
        # Mock the repository save method
        self.login_log_repo_mock.save.return_value = mock_log
        
        # Act
        result = self.service.create_login_log(
            status=status,
            login_type=login_type,
            ipaddress=ipaddress,
            browser=browser,
            system=system,
            agent=agent,
            creator=creator_id
        )
        
        # Assert
        self.assertEqual(result["status"], status)
        self.assertEqual(result["login_type"], login_type)
        self.user_repo_mock.find_by_id.assert_called_once_with(creator_id)
        mock_login_log_class.assert_called_once_with(
            status=status,
            login_type=login_type,
            ipaddress=ipaddress,
            browser=browser,
            system=system,
            agent=agent,
            creator=mock_user
        )
        self.login_log_repo_mock.save.assert_called_once_with(mock_log)
    
    def test_get_login_log_success(self):
        # Arrange
        log_id = 1
        status = True
        login_type = 1
        ipaddress = "192.168.1.1"
        browser = "Chrome"
        system = "Windows"
        agent = "Mozilla/5.0"
        creator_id = 1
        
        # Create a mock user object
        mock_user = Mock(spec=User)
        mock_user.id = creator_id
        
        # Create a mock login log object
        mock_log = Mock(spec=LoginLog)
        mock_log.id = log_id
        mock_log.status = status
        mock_log.login_type = login_type
        mock_log.ipaddress = ipaddress
        mock_log.browser = browser
        mock_log.system = system
        mock_log.agent = agent
        mock_log.creator = mock_user
        mock_log.created_time = datetime.now()
        mock_log.updated_time = datetime.now()
        
        # Mock login_log_repo.find_by_id to return the mock log
        self.login_log_repo_mock.find_by_id.return_value = mock_log
        
        # Act
        result = self.service.get_login_log(log_id)
        
        # Assert
        self.assertEqual(result["status"], status)
        self.assertEqual(result["login_type"], login_type)
        self.login_log_repo_mock.find_by_id.assert_called_once_with(log_id)
    
    def test_list_login_logs_success(self):
        # Arrange
        creator_id = 1
        
        # Create a mock user object
        mock_user = Mock(spec=User)
        mock_user.id = creator_id
        
        # Create mock login log objects
        mock_log1 = Mock(spec=LoginLog)
        mock_log1.id = 1
        mock_log1.status = True
        mock_log1.login_type = 1
        mock_log1.ipaddress = "192.168.1.1"
        mock_log1.browser = "Chrome"
        mock_log1.system = "Windows"
        mock_log1.agent = "Mozilla/5.0"
        mock_log1.creator = mock_user
        mock_log1.created_time = datetime.now()
        mock_log1.updated_time = datetime.now()
        
        mock_log2 = Mock(spec=LoginLog)
        mock_log2.id = 2
        mock_log2.status = False
        mock_log2.login_type = 2
        mock_log2.ipaddress = "192.168.1.2"
        mock_log2.browser = "Firefox"
        mock_log2.system = "Mac"
        mock_log2.agent = "Mozilla/5.0"
        mock_log2.creator = mock_user
        mock_log2.created_time = datetime.now()
        mock_log2.updated_time = datetime.now()
        
        # Mock login_log_repo.list_all to return the mock logs
        self.login_log_repo_mock.list_all.return_value = [mock_log1, mock_log2]
        
        # Act
        result = self.service.list_login_logs()
        
        # Assert
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["status"], True)
        self.assertEqual(result[1]["status"], False)
        self.login_log_repo_mock.list_all.assert_called_once()
    
    def test_update_login_log_success(self):
        # Arrange
        log_id = 1
        status = False
        login_type = 2
        
        # Create a mock login log object
        mock_log = Mock(spec=LoginLog)
        mock_log.status = True
        mock_log.login_type = 1
        
        # Mock login_log_repo.find_by_id to return the mock log
        self.login_log_repo_mock.find_by_id.return_value = mock_log
        
        # Mock the repository save method
        self.login_log_repo_mock.save.return_value = mock_log
        
        # Act
        result = self.service.update_login_log(
            log_id=log_id,
            status=status,
            login_type=login_type
        )
        
        # Assert
        self.assertEqual(result["status"], status)
        self.assertEqual(result["login_type"], login_type)
        self.login_log_repo_mock.find_by_id.assert_called_once_with(log_id)
        self.login_log_repo_mock.save.assert_called_once_with(mock_log)
    
    def test_delete_login_log_success(self):
        # Arrange
        log_id = 1
        self.login_log_repo_mock.delete.return_value = True
        
        # Act
        result = self.service.delete_login_log(log_id)
        
        # Assert
        self.assertTrue(result)
        self.login_log_repo_mock.delete.assert_called_once_with(log_id)
    
    def test_create_login_log_user_not_found(self):
        # Arrange
        status = True
        login_type = 1
        creator_id = 1
        
        # Mock user_repo.find_by_id to return None (user not found)
        self.user_repo_mock.find_by_id.return_value = None
        
        # Act & Assert
        with self.assertRaises(BusinessException):
            self.service.create_login_log(
                status=status,
                login_type=login_type,
                creator_id=creator_id
            )
    
    def test_get_login_log_not_found(self):
        # Arrange
        log_id = 1
        self.login_log_repo_mock.find_by_id.return_value = None
        
        # Act & Assert
        with self.assertRaises(BusinessException):
            self.service.get_login_log(log_id)
    
    def test_update_login_log_not_found(self):
        # Arrange
        log_id = 1
        status = False
        self.login_log_repo_mock.find_by_id.return_value = None
        
        # Act & Assert
        with self.assertRaises(BusinessException):
            self.service.update_login_log(log_id=log_id, status=status)
    
    def test_delete_login_log_not_found(self):
        # Arrange
        log_id = 1
        self.login_log_repo_mock.delete.return_value = False
        
        # Act & Assert
        with self.assertRaises(BusinessException):
            self.service.delete_login_log(log_id)