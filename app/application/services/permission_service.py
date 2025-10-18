"""
权限相关应用服务
"""

from app.domain.repositories.permission_repository import PermissionRepository
from django.contrib.auth.models import Permission
from app.common.exception.exceptions import BusinessException
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

    def update_permission(self, permission_id: int, name: str = None, codename: str = None, content_type=None) -> dict:
        """
        更新权限信息
        """
        permission = self.permission_repo.find_by_id(permission_id)
        if not permission:
            raise BusinessException(f"Permission with id '{permission_id}' not found.")
        
        if name is not None:
            permission.name = name
        if codename is not None:
            permission.codename = codename
        if content_type is not None:
            permission.content_type = content_type
        
        self.permission_repo.save(permission)
        return {
            "id": permission.pk,
            "name": permission.name,
            "codename": permission.codename,
        }

    def delete_permission(self, permission_id: int) -> bool:
        """
        删除权限
        """
        result = self.permission_repo.delete(permission_id)
        if not result:
            raise BusinessException(f"Permission with id '{permission_id}' not found.")
        return result

    def list_permissions(self) -> List[dict]:
        """
        获取所有权限列表
        """
        permissions = self.permission_repo.list_all()
        return [
            {
                "id": permission.pk,
                "name": permission.name,
                "codename": permission.codename,
            }
            for permission in permissions
        ]