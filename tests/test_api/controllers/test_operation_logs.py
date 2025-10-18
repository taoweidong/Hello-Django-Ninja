# test_operation_logs_controller.py
from unittest.mock import Mock, patch
from django.test import TestCase
from app.application.services.operation_log_service import OperationLogService
from app.domain.models.operation_log import OperationLog
from app.domain.models.user import User
from app.common.exception.exceptions import BusinessException
from datetime import datetime


class TestOperationLogsController(TestCase):
    def setUp(self):
        self.service = OperationLogService()
    
    def test_create_operation_log_success(self):
        # Arrange
        module = "User"
        path = "/api/users"
        method = "POST"
        ipaddress = "192.168.1.1"
        browser = "Chrome"
        system = "Windows"
        response_code = 201
        creator_id = 1
        
        # Mock User.objects.get to return a mock user
        with patch('app.domain.models.user.User.objects.get') as mock_user_get:
            mock_user = Mock(spec=User)
            mock_user.id = creator_id
            mock_user_get.return_value = mock_user
            
            # Mock OperationLog constructor and save method
            with patch('app.domain.models.operation_log.OperationLog') as MockOperationLog:
                mock_log_instance = Mock(spec=OperationLog)
                mock_log_instance.id = 1
                mock_log_instance.module = module
                mock_log_instance.path = path
                mock_log_instance.method = method
                mock_log_instance.ipaddress = ipaddress
                mock_log_instance.browser = browser
                mock_log_instance.system = system
                mock_log_instance.response_code = response_code
                mock_log_instance.creator = mock_user
                mock_log_instance.created_time = datetime.now()
                mock_log_instance.updated_time = datetime.now()
                
                MockOperationLog.return_value = mock_log_instance
                mock_log_instance.save.return_value = None
                
                # Act
                result = self.service.create_operation_log(
                    module=module,
                    path=path,
                    method=method,
                    ipaddress=ipaddress,
                    browser=browser,
                    system=system,
                    response_code=response_code,
                    creator_id=creator_id
                )
                
                # Assert
                self.assertEqual(result["module"], module)
                self.assertEqual(result["path"], path)
                MockOperationLog.assert_called_once_with(
                    module=module,
                    path=path,
                    body=None,
                    method=method,
                    ipaddress=ipaddress,
                    browser=browser,
                    system=system,
                    response_code=response_code,
                    response_result=None,
                    status_code=None,
                    description=None,
                    creator=mock_user
                )
                mock_log_instance.save.assert_called_once()
    
    def test_get_operation_log_success(self):
        # Arrange
        log_id = 1
        module = "User"
        path = "/api/users"
        method = "POST"
        ipaddress = "192.168.1.1"
        browser = "Chrome"
        system = "Windows"
        response_code = 201
        creator_id = 1
        
        # Create a mock user object
        mock_user = Mock(spec=User)
        mock_user.id = creator_id
        
        # Mock OperationLog.objects.get to return a mock log
        with patch('app.domain.models.operation_log.OperationLog.objects.get') as mock_log_get:
            mock_log = Mock(spec=OperationLog)
            mock_log.id = log_id
            mock_log.module = module
            mock_log.path = path
            mock_log.method = method
            mock_log.ipaddress = ipaddress
            mock_log.browser = browser
            mock_log.system = system
            mock_log.response_code = response_code
            mock_log.creator = mock_user
            mock_log.created_time = datetime.now()
            mock_log.updated_time = datetime.now()
            
            mock_log_get.return_value = mock_log
            
            # Act
            result = self.service.get_operation_log(log_id)
            
            # Assert
            self.assertEqual(result["module"], module)
            self.assertEqual(result["path"], path)
            mock_log_get.assert_called_once_with(id=log_id)
    
    def test_list_operation_logs_success(self):
        # Arrange
        creator_id = 1
        
        # Create a mock user object
        mock_user = Mock(spec=User)
        mock_user.id = creator_id
        
        # Create mock operation log objects
        mock_log1 = Mock(spec=OperationLog)
        mock_log1.id = 1
        mock_log1.module = "User"
        mock_log1.path = "/api/users"
        mock_log1.method = "POST"
        mock_log1.ipaddress = "192.168.1.1"
        mock_log1.browser = "Chrome"
        mock_log1.system = "Windows"
        mock_log1.response_code = 201
        mock_log1.creator = mock_user
        mock_log1.created_time = datetime.now()
        mock_log1.updated_time = datetime.now()
        
        mock_log2 = Mock(spec=OperationLog)
        mock_log2.id = 2
        mock_log2.module = "Role"
        mock_log2.path = "/api/roles"
        mock_log2.method = "GET"
        mock_log2.ipaddress = "192.168.1.2"
        mock_log2.browser = "Firefox"
        mock_log2.system = "Mac"
        mock_log2.response_code = 200
        mock_log2.creator = mock_user
        mock_log2.created_time = datetime.now()
        mock_log2.updated_time = datetime.now()
        
        # Mock OperationLog.objects.all to return the mock logs
        with patch('app.domain.models.operation_log.OperationLog.objects.all', return_value=[mock_log1, mock_log2]):
            # Act
            result = self.service.list_operation_logs()
            
            # Assert
            self.assertEqual(len(result), 2)
            self.assertEqual(result[0]["module"], "User")
            self.assertEqual(result[1]["module"], "Role")
    
    def test_update_operation_log_success(self):
        # Arrange
        log_id = 1
        module = "Updated User"
        path = "/api/users/1"
        
        # Mock OperationLog.objects.get to return a mock log
        with patch('app.domain.models.operation_log.OperationLog.objects.get') as mock_log_get:
            mock_log = Mock(spec=OperationLog)
            mock_log.module = "User"
            mock_log.path = "/api/users"
            
            mock_log_get.return_value = mock_log
            mock_log.save.return_value = None
            
            # Act
            result = self.service.update_operation_log(
                log_id=log_id,
                module=module,
                path=path
            )
            
            # Assert
            self.assertEqual(result["module"], module)
            self.assertEqual(result["path"], path)
            mock_log_get.assert_called_once_with(id=log_id)
            mock_log.save.assert_called_once()
    
    def test_delete_operation_log_success(self):
        # Arrange
        log_id = 1
        
        # Mock OperationLog.objects.get to return a mock log
        with patch('app.domain.models.operation_log.OperationLog.objects.get') as mock_log_get:
            mock_log = Mock(spec=OperationLog)
            mock_log.delete.return_value = None
            
            mock_log_get.return_value = mock_log
            
            # Act
            result = self.service.delete_operation_log(log_id)
            
            # Assert
            self.assertTrue(result)
            mock_log_get.assert_called_once_with(id=log_id)
            mock_log.delete.assert_called_once()
    
    def test_create_operation_log_user_not_found(self):
        # Arrange
        module = "User"
        path = "/api/users"
        creator_id = 1
        
        # Mock User.objects.get to raise DoesNotExist
        with patch('app.domain.models.user.User.objects.get') as mock_user_get:
            # 创建一个DoesNotExist异常实例
            does_not_exist_exception = Exception("User does not exist")
            mock_user_get.side_effect = does_not_exist_exception
            
            # Act & Assert
            with self.assertRaises(BusinessException):
                self.service.create_operation_log(
                    module=module,
                    path=path,
                    creator_id=creator_id
                )
    
    def test_get_operation_log_not_found(self):
        # Arrange
        log_id = 1
        
        # Mock OperationLog.objects.get to raise DoesNotExist
        with patch('app.domain.models.operation_log.OperationLog.objects.get') as mock_log_get:
            # 创建一个DoesNotExist异常实例
            does_not_exist_exception = Exception("OperationLog does not exist")
            mock_log_get.side_effect = does_not_exist_exception
            
            # Act & Assert
            with self.assertRaises(BusinessException):
                self.service.get_operation_log(log_id)
    
    def test_update_operation_log_not_found(self):
        # Arrange
        log_id = 1
        module = "Updated User"
        
        # Mock OperationLog.objects.get to raise DoesNotExist
        with patch('app.domain.models.operation_log.OperationLog.objects.get') as mock_log_get:
            # 创建一个DoesNotExist异常实例
            does_not_exist_exception = Exception("OperationLog does not exist")
            mock_log_get.side_effect = does_not_exist_exception
            
            # Act & Assert
            with self.assertRaises(BusinessException):
                self.service.update_operation_log(log_id=log_id, module=module)
    
    def test_delete_operation_log_not_found(self):
        # Arrange
        log_id = 1
        
        # Mock OperationLog.objects.get to raise DoesNotExist
        with patch('app.domain.models.operation_log.OperationLog.objects.get') as mock_log_get:
            # 创建一个DoesNotExist异常实例
            does_not_exist_exception = Exception("OperationLog does not exist")
            mock_log_get.side_effect = does_not_exist_exception
            
            # Act & Assert
            with self.assertRaises(BusinessException):
                self.service.delete_operation_log(log_id)