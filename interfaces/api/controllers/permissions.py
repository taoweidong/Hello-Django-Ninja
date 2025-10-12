"""
权限管理 API Controller
"""

from ninja_extra import api_controller, http_get, permissions
from ninja import Schema
from application.services.permission_service import PermissionService
from interfaces.api.schemas import PermissionOut
from common.exceptions import BusinessException
from infrastructure.persistence.repos.permission_repo_impl import (
    DjangoORMPermissionRepository,
)


@api_controller("/permissions", permissions=[permissions.IsAuthenticated])
class PermissionsController:
    def __init__(self):
        # 实例化仓储实现
        permission_repo = DjangoORMPermissionRepository()
        # 实例化应用服务
        self.service = PermissionService(permission_repo)

    @http_get("/{int:permission_id}", response=PermissionOut)
    def get_permission(self, permission_id: int):
        try:
            permission_data = self.service.get_permission_by_id(permission_id)
            return permission_data
        except BusinessException as e:
            return 400, {"message": str(e)}

    @http_get("/", response=list[PermissionOut])
    def list_permissions(self):
        # 实现列出所有权限的逻辑
        pass
