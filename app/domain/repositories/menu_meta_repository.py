"""
菜单元数据仓储接口
"""

from abc import ABC, abstractmethod
from typing import Optional, List, Union
from app.domain.models.menu_meta import MenuMeta


class MenuMetaRepository(ABC):
    @abstractmethod
    def save(self, entity: MenuMeta) -> None:
        pass

    @abstractmethod
    def find_by_id(self, entity_id: Union[int, str]) -> Optional[MenuMeta]:
        pass

    @abstractmethod
    def delete(self, entity_id: Union[int, str]) -> bool:
        pass

    @abstractmethod
    def list_all(self) -> List[MenuMeta]:
        pass