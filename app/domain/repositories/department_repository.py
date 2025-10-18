"""
部门仓储接口
"""

from abc import ABC, abstractmethod
from typing import Optional, List, Union
from app.domain.models.department import Department


class DepartmentRepository(ABC):
    @abstractmethod
    def save(self, entity: Department) -> None:
        pass

    @abstractmethod
    def find_by_id(self, entity_id: Union[int, str]) -> Optional[Department]:
        pass

    @abstractmethod
    def find_by_code(self, code: str) -> Optional[Department]:
        pass

    @abstractmethod
    def delete(self, entity_id: Union[int, str]) -> bool:
        pass

    @abstractmethod
    def list_all(self) -> List[Department]:
        pass