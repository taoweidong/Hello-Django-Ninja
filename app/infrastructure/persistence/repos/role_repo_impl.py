"""
角色仓储实现
"""

from app.domain.repositories.role_repository import RoleRepository
from app.domain.models.role import Role
from django.core.exceptions import ObjectDoesNotExist
from typing import Optional, List, Union
from django.apps import apps
from .base_repository import BaseRepository


class DjangoORMRoleRepository(RoleRepository, BaseRepository[Role]):
    def __init__(self):
        # 获取实际的 Django 模型类
        self.RoleModel = apps.get_model("domain", "Role")
        # 初始化基类
        BaseRepository.__init__(self, self.RoleModel)

    def save(self, role: Role) -> None:
        role.save()

    def find_by_id(self, role_id: Union[str, int]) -> Optional[Role]:
        try:
            # 如果传入的是整数，转换为字符串
            if isinstance(role_id, int):
                role_id = str(role_id)
            return self.RoleModel.objects.get(pk=role_id)
        except ObjectDoesNotExist:
            return None

    def find_by_name(self, name: str) -> Optional[Role]:
        try:
            return self.RoleModel.objects.get(name=name)
        except ObjectDoesNotExist:
            return None

    def delete(self, role_id: Union[str, int]) -> bool:
        try:
            # 如果传入的是整数，转换为字符串
            if isinstance(role_id, int):
                role_id = str(role_id)
            role = self.RoleModel.objects.get(pk=role_id)
            role.delete()
            return True
        except ObjectDoesNotExist:
            return False

    def list_all(self) -> List[Role]:
        return list(self.RoleModel.objects.all())

    def assign_permissions(self, role_id: Union[str, int], permission_ids: List[int]) -> None:
        try:
            # 如果传入的是整数，转换为字符串
            if isinstance(role_id, int):
                role_id = str(role_id)
            role = self.RoleModel.objects.get(pk=role_id)
            role.permissions.set(permission_ids)
        except ObjectDoesNotExist:
            pass  # 或抛出异常