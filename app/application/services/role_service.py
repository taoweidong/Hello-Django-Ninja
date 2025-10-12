"""
角色相关应用服务
"""

from app.domain.repositories.role_repository import RoleRepository
from app.domain.models.role import Role
from app.common.exceptions import BusinessException
from typing import List


class RoleService:
    def __init__(self, role_repo: RoleRepository):
        self.role_repo = role_repo

    def create_role(self, name: str, description: str) -> dict:
        """
        创建角色
        """
        if self.role_repo.find_by_name(name):
            raise BusinessException(f"Role with name '{name}' already exists.")
        role = Role(name=name, description=description)
        self.role_repo.save(role)
        return {"id": role.id, "name": role.name, "description": role.description}

    def assign_permissions_to_role(
        self, role_id: int, permission_ids: List[int]
    ) -> None:
        """
        为角色分配权限
        """
        # 业务逻辑校验
        self.role_repo.assign_permissions(role_id, permission_ids)