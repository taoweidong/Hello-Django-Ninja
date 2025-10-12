"""
权限仓储实现
"""

from domain.repositories.permission_repository import PermissionRepository
from django.contrib.auth.models import Permission
from django.core.exceptions import ObjectDoesNotExist
from typing import Optional, List


class DjangoORMPermissionRepository(PermissionRepository):
    def save(self, permission: Permission) -> None:
        permission.save()

    def find_by_id(self, permission_id: int) -> Optional[Permission]:
        try:
            return Permission.objects.get(pk=permission_id)
        except ObjectDoesNotExist:
            return None

    def find_by_codename(self, codename: str) -> Optional[Permission]:
        try:
            return Permission.objects.get(codename=codename)
        except ObjectDoesNotExist:
            return None

    def delete(self, permission_id: int) -> bool:
        try:
            permission = Permission.objects.get(pk=permission_id)
            permission.delete()
            return True
        except ObjectDoesNotExist:
            return False

    def list_all(self) -> List[Permission]:
        return list(Permission.objects.all())
