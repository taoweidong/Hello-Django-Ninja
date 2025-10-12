"""
角色管理 API Controller
"""

from ninja_extra import api_controller, http_get, http_post, permissions
from ninja import Schema
from app.application.services.role_service import RoleService
from app.interfaces.api.schemas import RoleOut, RoleCreate
from app.common.exceptions import BusinessException
from app.infrastructure.persistence.repos.role_repo_impl import DjangoORMRoleRepository


@api_controller("/roles", permissions=[permissions.IsAuthenticated])
class RolesController:
    def __init__(self):
        # 实例化仓储实现
        role_repo = DjangoORMRoleRepository()
        # 实例化应用服务
        self.service = RoleService(role_repo)

    @http_post("/", response={201: RoleOut})
    def create_role(self, payload: RoleCreate):
        try:
            role_data = self.service.create_role(payload.name, payload.description)
            return 201, role_data
        except BusinessException as e:
            return 400, {"message": str(e)}

    @http_get("/{int:role_id}", response=RoleOut)
    def get_role(self, role_id: int):
        # 实现获取角色的逻辑
        pass

    @http_get("/", response=list[RoleOut])
    def list_roles(self):
        # 实现列出所有角色的逻辑
        pass