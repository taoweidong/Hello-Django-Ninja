"""
系统配置仓储接口
"""

from abc import ABC, abstractmethod
from typing import Optional, List, Union
from app.domain.models.system_config import SystemConfig


class SystemConfigRepository(ABC):
    @abstractmethod
    def save(self, entity: SystemConfig) -> None:
        pass

    @abstractmethod
    def find_by_id(self, entity_id: Union[int, str]) -> Optional[SystemConfig]:
        pass

    @abstractmethod
    def find_by_key(self, key: str) -> Optional[SystemConfig]:
        pass

    @abstractmethod
    def delete(self, entity_id: Union[int, str]) -> bool:
        pass

    @abstractmethod
    def list_all(self) -> List[SystemConfig]:
        pass