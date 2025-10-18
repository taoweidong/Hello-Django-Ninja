"""
登录日志仓储接口
"""

from abc import ABC, abstractmethod
from typing import Optional, List, Union
from app.domain.models.login_log import LoginLog


class LoginLogRepository(ABC):
    @abstractmethod
    def save(self, entity: LoginLog) -> None:
        pass

    @abstractmethod
    def find_by_id(self, entity_id: Union[int, str]) -> Optional[LoginLog]:
        pass

    @abstractmethod
    def delete(self, entity_id: Union[int, str]) -> bool:
        pass

    @abstractmethod
    def list_all(self) -> List[LoginLog]:
        pass