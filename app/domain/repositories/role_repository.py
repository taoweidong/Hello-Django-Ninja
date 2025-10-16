"""
角色仓储接口
"""

from abc import ABC, abstractmethod
from typing import Optional, List, Union
from app.domain.models.role import Role


class RoleRepository(ABC):
    @abstractmethod
    def save(self, role: Role) -> None:
        pass

    @abstractmethod
    def find_by_id(self, role_id: Union[str, int]) -> Optional[Role]:
        pass

    @abstractmethod
    def find_by_name(self, name: str) -> Optional[Role]:
        pass

    @abstractmethod
    def delete(self, role_id: Union[str, int]) -> bool:
        pass

    @abstractmethod
    def list_all(self) -> List[Role]:
        pass

    @abstractmethod
    def assign_permissions(self, role_id: Union[str, int], permission_ids: List[int]) -> None:
        pass