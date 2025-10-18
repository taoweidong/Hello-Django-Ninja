"""
角色管理 API Controller
"""

from ninja_extra import api_controller, http_get, http_post, http_put, http_delete
from ninja_jwt.authentication import JWTAuth

from app.application.services.role_service import RoleService
from app.common.exception.exceptions import BusinessException
from app.infrastructure.persistence.repos.role_repo_impl import DjangoORMRoleRepository
from app.api.schemas import RoleOut, RoleCreate, RoleUpdate, ApiResponse
from app.common.api_response import success


@api_controller("/roles", auth=JWTAuth())
class RolesController:
    def __init__(self):
        # 实例化仓储实现
        role_repo = DjangoORMRoleRepository()
        # 实例化应用服务
        self.service = RoleService(role_repo)

    @http_post("/", response=ApiResponse[RoleOut])
    def create_role(self, payload: RoleCreate):
        role_data = self.service.create_role(payload.name, payload.description)
        return success(role_data, "Role created successfully", 201)

    @http_get("/{role_id}", response=ApiResponse[RoleOut])
    def get_role(self, role_id: str):
        # 通过service层获取角色数据
        role_data = self.service.get_role(role_id)
        if role_data:
            return success(role_data, "Role retrieved successfully")
        else:
            # 这个异常将由全局异常处理器处理
            raise BusinessException("Role not found")

    @http_get("/", response=ApiResponse[list[RoleOut]])
    def list_roles(self):
        # 通过service层获取所有角色数据
        roles_data = self.service.list_roles()
        return success(roles_data, "Roles retrieved successfully")

    @http_put("/{role_id}", response=ApiResponse[RoleOut])
    def update_role(self, role_id: str, payload: RoleUpdate):
        # 只传递非空值进行更新
        update_kwargs = {}
        if payload.name is not None:
            update_kwargs['name'] = payload.name
        if payload.description is not None:
            update_kwargs['description'] = payload.description
            
        role_data = self.service.update_role(
            role_id, 
            **update_kwargs
        )
        return success(role_data, "Role updated successfully")

    @http_delete("/{role_id}", response=ApiResponse[None])
    def delete_role(self, role_id: str):
        self.service.delete_role(role_id)
        return success(None, "Role deleted successfully")