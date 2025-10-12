"""
权限相关应用服务
"""

from app.domain.repositories.permission_repository import PermissionRepository
from django.contrib.auth.models import Permission
from app.common.exceptions import BusinessException
from typing import List


class PermissionService:
    def __init__(self, permission_repo: PermissionRepository):
        self.permission_repo = permission_repo

    def create_permission(self, name: str, codename: str, content_type) -> dict:
        """
        创建权限
        """
        if self.permission_repo.find_by_codename(codename):
            raise BusinessException(
                f"Permission with codename '{codename}' already exists."
            )
        permission = Permission(name=name, codename=codename, content_type=content_type)
        self.permission_repo.save(permission)
        return {
            "id": permission.pk,
            "name": permission.name,
            "codename": permission.codename,
        }

    def get_permission_by_id(self, permission_id: int) -> dict:
        """
        根据ID获取权限
        """
        permission = self.permission_repo.find_by_id(permission_id)
        if not permission:
            raise BusinessException(f"Permission with id '{permission_id}' not found.")
        return {
            "id": permission.pk,
            "name": permission.name,
            "codename": permission.codename,
        }