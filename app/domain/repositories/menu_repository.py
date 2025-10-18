"""
菜单元数据仓储接口
"""

from abc import ABC, abstractmethod
from typing import Optional, List, Union
from app.domain.models.menu import Menu


class MenuRepository(ABC):
    @abstractmethod
    def save(self, entity: Menu) -> None:
        pass

    @abstractmethod
    def find_by_id(self, entity_id: Union[int, str]) -> Optional[Menu]:
        pass

    @abstractmethod
    def find_by_name(self, name: str) -> Optional[Menu]:
        pass

    @abstractmethod
    def delete(self, entity_id: Union[int, str]) -> bool:
        pass

    @abstractmethod
    def list_all(self) -> List[Menu]:
        pass