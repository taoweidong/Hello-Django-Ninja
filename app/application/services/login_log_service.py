"""
登录日志相关应用服务
"""

from app.domain.models.login_log import LoginLog
from app.domain.models.user import User
from app.common.exceptions import BusinessException
from typing import List, Optional


class LoginLogService:
    def __init__(self):
        pass

    def create_login_log(
        self,
        status: bool,
        login_type: int,
        ipaddress: Optional[str] = None,
        browser: Optional[str] = None,
        system: Optional[str] = None,
        agent: Optional[str] = None,
        description: Optional[str] = None,
        creator_id: Optional[int] = None
    ) -> dict:
        """
        创建登录日志
        """
        # 检查creator_id是否存在
        creator = None
        if creator_id:
            try:
                creator = User.objects.get(id=creator_id)
            except User.DoesNotExist:
                raise BusinessException(f"User with id '{creator_id}' not found.")
        
        log = LoginLog(
            status=status,
            login_type=login_type,
            ipaddress=ipaddress,
            browser=browser,
            system=system,
            agent=agent,
            description=description,
            creator=creator
        )
        log.save()
        return self._login_log_to_dict(log)

    def get_login_log(self, log_id: int) -> dict:
        """
        根据ID获取登录日志
        """
        try:
            log = LoginLog.objects.get(id=log_id)
            return self._login_log_to_dict(log)
        except LoginLog.DoesNotExist:
            raise BusinessException(f"LoginLog with id '{log_id}' not found.")

    def update_login_log(
        self,
        log_id: int,
        status: Optional[bool] = None,
        login_type: Optional[int] = None,
        ipaddress: Optional[str] = None,
        browser: Optional[str] = None,
        system: Optional[str] = None,
        agent: Optional[str] = None,
        description: Optional[str] = None
    ) -> dict:
        """
        更新登录日志信息
        """
        try:
            log = LoginLog.objects.get(id=log_id)
            
            if status is not None:
                log.status = status
            if login_type is not None:
                log.login_type = login_type
            if ipaddress is not None:
                log.ipaddress = ipaddress
            if browser is not None:
                log.browser = browser
            if system is not None:
                log.system = system
            if agent is not None:
                log.agent = agent
            if description is not None:
                log.description = description
            
            log.save()
            return self._login_log_to_dict(log)
        except LoginLog.DoesNotExist:
            raise BusinessException(f"LoginLog with id '{log_id}' not found.")

    def delete_login_log(self, log_id: int) -> bool:
        """
        删除登录日志
        """
        try:
            log = LoginLog.objects.get(id=log_id)
            log.delete()
            return True
        except LoginLog.DoesNotExist:
            raise BusinessException(f"LoginLog with id '{log_id}' not found.")

    def list_login_logs(self) -> List[dict]:
        """
        获取所有登录日志列表
        """
        logs = LoginLog.objects.all()
        return [self._login_log_to_dict(log) for log in logs]

    def _login_log_to_dict(self, log: LoginLog) -> dict:
        """
        将LoginLog对象转换为字典
        """
        return {
            "id": log.id,
            "status": log.status,
            "login_type": log.login_type,
            "ipaddress": log.ipaddress,
            "browser": log.browser,
            "system": log.system,
            "agent": log.agent,
            "description": log.description,
            "creator_id": log.creator.id if log.creator else None,
            "created_time": log.created_time,
            "updated_time": log.updated_time
        }