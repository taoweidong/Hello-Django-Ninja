"""
角色仓储实现
"""

from domain.repositories.role_repository import RoleRepository
from domain.models.role import Role
from django.core.exceptions import ObjectDoesNotExist
from typing import Optional, List
from django.apps import apps


class DjangoORMRoleRepository(RoleRepository):
    def __init__(self):
        # 获取实际的 Django 模型类
        self.RoleModel = apps.get_model("domain", "Role")

    def save(self, role: Role) -> None:
        role.save()

    def find_by_id(self, role_id: int) -> Optional[Role]:
        try:
            return self.RoleModel.objects.get(pk=role_id)
        except ObjectDoesNotExist:
            return None

    def find_by_name(self, name: str) -> Optional[Role]:
        try:
            return self.RoleModel.objects.get(name=name)
        except ObjectDoesNotExist:
            return None

    def delete(self, role_id: int) -> bool:
        try:
            role = self.RoleModel.objects.get(pk=role_id)
            role.delete()
            return True
        except ObjectDoesNotExist:
            return False

    def list_all(self) -> List[Role]:
        return list(self.RoleModel.objects.all())

    def assign_permissions(self, role_id: int, permission_ids: List[int]) -> None:
        try:
            role = self.RoleModel.objects.get(pk=role_id)
            role.permissions.set(permission_ids)
        except ObjectDoesNotExist:
            pass  # 或抛出异常
