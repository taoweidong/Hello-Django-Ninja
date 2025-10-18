"""
操作日志相关应用服务
"""

from app.domain.models.operation_log import OperationLog
from app.domain.models.user import User
from app.common.exception.exceptions import BusinessException
from typing import List, Optional


class OperationLogService:
    def __init__(self):
        pass

    def create_operation_log(
        self,
        module: Optional[str] = None,
        path: Optional[str] = None,
        body: Optional[str] = None,
        method: Optional[str] = None,
        ipaddress: Optional[str] = None,
        browser: Optional[str] = None,
        system: Optional[str] = None,
        response_code: Optional[int] = None,
        response_result: Optional[str] = None,
        status_code: Optional[int] = None,
        description: Optional[str] = None,
        creator_id: Optional[int] = None
    ) -> dict:
        """
        创建操作日志
        """
        # 检查creator_id是否存在
        creator = None
        if creator_id:
            try:
                creator = User.objects.get(id=creator_id)
            except User.DoesNotExist:
                raise BusinessException(f"User with id '{creator_id}' not found.")
        
        log = OperationLog(
            module=module,
            path=path,
            body=body,
            method=method,
            ipaddress=ipaddress,
            browser=browser,
            system=system,
            response_code=response_code,
            response_result=response_result,
            status_code=status_code,
            description=description,
            creator=creator
        )
        log.save()
        return self._operation_log_to_dict(log)

    def get_operation_log(self, log_id: int) -> dict:
        """
        根据ID获取操作日志
        """
        try:
            log = OperationLog.objects.get(id=log_id)
            return self._operation_log_to_dict(log)
        except OperationLog.DoesNotExist:
            raise BusinessException(f"OperationLog with id '{log_id}' not found.")

    def update_operation_log(
        self,
        log_id: int,
        module: Optional[str] = None,
        path: Optional[str] = None,
        body: Optional[str] = None,
        method: Optional[str] = None,
        ipaddress: Optional[str] = None,
        browser: Optional[str] = None,
        system: Optional[str] = None,
        response_code: Optional[int] = None,
        response_result: Optional[str] = None,
        status_code: Optional[int] = None,
        description: Optional[str] = None
    ) -> dict:
        """
        更新操作日志信息
        """
        try:
            log = OperationLog.objects.get(id=log_id)
            
            if module is not None:
                log.module = module
            if path is not None:
                log.path = path
            if body is not None:
                log.body = body
            if method is not None:
                log.method = method
            if ipaddress is not None:
                log.ipaddress = ipaddress
            if browser is not None:
                log.browser = browser
            if system is not None:
                log.system = system
            if response_code is not None:
                log.response_code = response_code
            if response_result is not None:
                log.response_result = response_result
            if status_code is not None:
                log.status_code = status_code
            if description is not None:
                log.description = description
            
            log.save()
            return self._operation_log_to_dict(log)
        except OperationLog.DoesNotExist:
            raise BusinessException(f"OperationLog with id '{log_id}' not found.")

    def delete_operation_log(self, log_id: int) -> bool:
        """
        删除操作日志
        """
        try:
            log = OperationLog.objects.get(id=log_id)
            log.delete()
            return True
        except OperationLog.DoesNotExist:
            raise BusinessException(f"OperationLog with id '{log_id}' not found.")

    def list_operation_logs(self) -> List[dict]:
        """
        获取所有操作日志列表
        """
        logs = OperationLog.objects.all()
        return [self._operation_log_to_dict(log) for log in logs]

    def _operation_log_to_dict(self, log: OperationLog) -> dict:
        """
        将OperationLog对象转换为字典
        """
        return {
            "id": log.id,
            "module": log.module,
            "path": log.path,
            "body": log.body,
            "method": log.method,
            "ipaddress": log.ipaddress,
            "browser": log.browser,
            "system": log.system,
            "response_code": log.response_code,
            "response_result": log.response_result,
            "status_code": log.status_code,
            "description": log.description,
            "creator_id": log.creator.id if log.creator else None,
            "created_time": log.created_time,
            "updated_time": log.updated_time
        }