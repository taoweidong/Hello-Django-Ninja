"""
登录日志相关应用服务
"""
from django.utils import timezone

from app.domain.models.login_log import LoginLog
from app.domain.models.user import User
from app.domain.repositories.login_log_repository import LoginLogRepository
from app.domain.repositories.user_repository import UserRepository
from app.common.exception.exceptions import BusinessException
from typing import List, Optional


class LoginLogService:
    def __init__(self, login_log_repo: LoginLogRepository, user_repo: UserRepository):
        self.login_log_repo = login_log_repo
        self.user_repo = user_repo

    def create_login_log(
        self,
        status: bool,
        login_type: int,
        ipaddress: Optional[str] = None,
        browser: Optional[str] = None,
        system: Optional[str] = None,
        agent: Optional[str] = None,
        description: Optional[str] = None,
        creator: Optional[int] = None
    ) -> dict:
        """
        创建登录日志
        """
        log = LoginLog(
            status=status,
            login_type=login_type,
            ipaddress=ipaddress,
            browser=browser,
            system=system,
            agent=agent,
            creator=creator,
            created_time=timezone.now()
        )
        self.login_log_repo.save(log)
        return self._login_log_to_dict(log)

    def get_login_log(self, log_id: int) -> dict:
        """
        根据ID获取登录日志
        """
        log = self.login_log_repo.find_by_id(log_id)
        if not log:
            raise BusinessException(f"LoginLog with id '{log_id}' not found.")
        return self._login_log_to_dict(log)

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
        log = self.login_log_repo.find_by_id(log_id)
        if not log:
            raise BusinessException(f"LoginLog with id '{log_id}' not found.")
        
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
        # description字段不存在于模型中
        
        self.login_log_repo.save(log)
        return self._login_log_to_dict(log)

    def delete_login_log(self, log_id: int) -> bool:
        """
        删除登录日志
        """
        result = self.login_log_repo.delete(log_id)
        if not result:
            raise BusinessException(f"LoginLog with id '{log_id}' not found.")
        return result

    def list_login_logs(self) -> List[dict]:
        """
        获取所有登录日志列表
        """
        logs = self.login_log_repo.list_all()
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
            # description字段不存在于模型中,
            "creator_id": log.creator.id if log.creator else None,
            "created_time": log.created_time,
            "updated_time": log.updated_time
        }