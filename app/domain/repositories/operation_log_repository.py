"""
操作日志仓储接口
"""

from abc import ABC, abstractmethod
from typing import Optional, List, Union
from app.domain.models.operation_log import OperationLog


class OperationLogRepository(ABC):
    @abstractmethod
    def save(self, entity: OperationLog) -> None:
        pass

    @abstractmethod
    def find_by_id(self, entity_id: Union[int, str]) -> Optional[OperationLog]:
        pass

    @abstractmethod
    def delete(self, entity_id: Union[int, str]) -> bool:
        pass

    @abstractmethod
    def list_all(self) -> List[OperationLog]:
        pass