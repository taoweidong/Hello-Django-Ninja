"""
角色相关应用服务
"""

from app.domain.repositories.role_repository import RoleRepository
from app.domain.models.role import Role
from app.common.exception.exceptions import BusinessException
from typing import List, Union


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

    def get_role(self, role_id: Union[str, int]) -> dict:
        """
        根据ID获取角色
        """
        # 如果传入的是整数，转换为字符串
        if isinstance(role_id, int):
            role_id = str(role_id)
            
        role = self.role_repo.find_by_id(role_id)
        if not role:
            raise BusinessException(f"Role with id '{role_id}' not found.")
        return {"id": role.id, "name": role.name, "description": role.description}

    def update_role(self, role_id: Union[str, int], name: str = None, description: str = None) -> dict:
        """
        更新角色信息
        """
        # 如果传入的是整数，转换为字符串
        if isinstance(role_id, int):
            role_id = str(role_id)
            
        role = self.role_repo.find_by_id(role_id)
        if not role:
            raise BusinessException(f"Role with id '{role_id}' not found.")
        
        if name is not None:
            role.name = name
        if description is not None:
            role.description = description
        
        self.role_repo.save(role)
        return {"id": role.id, "name": role.name, "description": role.description}

    def delete_role(self, role_id: Union[str, int]) -> bool:
        """
        删除角色
        """
        # 如果传入的是整数，转换为字符串
        if isinstance(role_id, int):
            role_id = str(role_id)
            
        result = self.role_repo.delete(role_id)
        if not result:
            raise BusinessException(f"Role with id '{role_id}' not found.")
        return result

    def list_roles(self) -> List[dict]:
        """
        获取所有角色列表
        """
        roles = self.role_repo.list_all()
        return [{"id": role.id, "name": role.name, "description": role.description} for role in roles]

    def assign_permissions_to_role(
        self, role_id: Union[str, int], permission_ids: List[int]
    ) -> None:
        """
        为角色分配权限
        """
        # 如果传入的是整数，转换为字符串
        if isinstance(role_id, int):
            role_id = str(role_id)
            
        # 业务逻辑校验
        self.role_repo.assign_permissions(role_id, permission_ids)