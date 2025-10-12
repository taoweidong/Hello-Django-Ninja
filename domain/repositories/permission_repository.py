"""
权限仓储接口
"""

from abc import ABC, abstractmethod
from typing import Optional, List
from django.contrib.auth.models import Permission


class PermissionRepository(ABC):
    @abstractmethod
    def save(self, permission: Permission) -> None:
        pass

    @abstractmethod
    def find_by_id(self, permission_id: int) -> Optional[Permission]:
        pass

    @abstractmethod
    def find_by_codename(self, codename: str) -> Optional[Permission]:
        pass

    @abstractmethod
    def delete(self, permission_id: int) -> bool:
        pass

    @abstractmethod
    def list_all(self) -> List[Permission]:
        pass
