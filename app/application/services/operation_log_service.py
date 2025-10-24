"""
操作日志相关应用服务
"""

from app.domain.models.operation_log import OperationLog
from app.domain.models.user import User
from app.common.exception.exceptions import BusinessException
from typing import List, Optional
from django.core.exceptions import ObjectDoesNotExist


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
                creator = User.objects.get(id=creator_id)  # type: ignore
            except ObjectDoesNotExist:
                raise BusinessException(f"User with id '{creator_id}' not found.")
        
        log = OperationLog(
            module=module,
            oper_url=path,  # 对应字段
            oper_param=body,  # 对应字段
            request_method=method,  # 对应字段
            oper_ip=ipaddress,  # 对应字段
            browser=browser,
            system=system,
            response_code=response_code,
            json_result=response_result,  # 对应字段
            status=bool(status_code) if status_code is not None else False,  # 对应字段
            description=description,
            user=creator  # 对应字段
        )
        log.save()
        return self._operation_log_to_dict(log)

    def get_operation_log(self, log_id: int) -> dict:
        """
        根据ID获取操作日志
        """
        try:
            log = OperationLog.objects.get(id=log_id)  # type: ignore
            return self._operation_log_to_dict(log)
        except ObjectDoesNotExist:
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
            log = OperationLog.objects.get(id=log_id)  # type: ignore
            
            if module is not None:
                log.module = module
            if path is not None:
                log.oper_url = path  # 对应字段
            if body is not None:
                log.oper_param = body  # 对应字段
            if method is not None:
                log.request_method = method  # 对应字段
            if ipaddress is not None:
                log.oper_ip = ipaddress  # 对应字段
            if browser is not None:
                log.browser = browser
            if system is not None:
                log.system = system
            if response_code is not None:
                log.response_code = response_code
            if response_result is not None:
                log.json_result = response_result  # 对应字段
            if status_code is not None:
                log.status = bool(status_code)  # 对应字段
            if description is not None:
                log.description = description
            
            log.save()
            return self._operation_log_to_dict(log)
        except ObjectDoesNotExist:
            raise BusinessException(f"OperationLog with id '{log_id}' not found.")

    def delete_operation_log(self, log_id: int) -> bool:
        """
        删除操作日志
        """
        try:
            log = OperationLog.objects.get(id=log_id)  # type: ignore
            log.delete()
            return True
        except ObjectDoesNotExist:
            raise BusinessException(f"OperationLog with id '{log_id}' not found.")

    def list_operation_logs(self) -> List[dict]:
        """
        获取所有操作日志列表
        """
        logs = OperationLog.objects.all()  # type: ignore
        return [self._operation_log_to_dict(log) for log in logs]

    def _operation_log_to_dict(self, log: OperationLog) -> dict:
        """
        将OperationLog对象转换为字典
        """
        # 获取用户ID，处理可能的外键关系
        creator_id = None
        if hasattr(log, 'user') and log.user:
            creator_id = getattr(log.user, 'id', None)
        
        # 处理状态码转换
        status_code = None
        if log.status is not None:
            # 将布尔值转换为整数
            status_code = 1 if log.status else 0
        
        return {
            "id": log.id,
            "module": log.module,
            "path": log.oper_url,  # 对应字段
            "body": log.oper_param,  # 对应字段
            "method": log.request_method,  # 对应字段
            "ipaddress": log.oper_ip,  # 对应字段
            "browser": getattr(log, 'browser', None),  # 可能不存在的字段
            "system": getattr(log, 'system', None),  # 可能不存在的字段
            "response_code": getattr(log, 'response_code', None),  # 可能不存在的字段
            "response_result": log.json_result,  # 对应字段
            "status_code": status_code,  # 对应字段
            "description": log.description,
            "creator_id": creator_id,  # 对应字段
            "created_time": log.created_time,
            "updated_time": getattr(log, 'updated_time', log.created_time)  # 可能不存在的字段
        }