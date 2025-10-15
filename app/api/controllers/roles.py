"""
角色管理 API Controller
"""

from ninja_extra import api_controller, http_get, http_post, http_put, http_delete, permissions
from ninja_jwt.authentication import JWTAuth

from app.application.services.role_service import RoleService
from app.common.exceptions import BusinessException
from app.infrastructure.persistence.repos.role_repo_impl import DjangoORMRoleRepository
from app.api.schemas import RoleOut, RoleCreate, RoleUpdate


@api_controller("/roles", auth=JWTAuth())
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

    @http_get("/{role_id}", response=RoleOut)
    def get_role(self, role_id: str):
        # 通过service层获取角色数据
        try:
            role_data = self.service.get_role(int(role_id))
            return role_data
        except BusinessException as e:
            return 400, {"message": str(e)}
        except Exception as e:
            return 400, {"message": str(e)}

    @http_get("/", response=list[RoleOut])
    def list_roles(self):
        # 通过service层获取所有角色数据
        try:
            roles_data = self.service.list_roles()
            return roles_data
        except Exception as e:
            return 400, {"message": str(e)}

    @http_put("/{role_id}", response=RoleOut)
    def update_role(self, role_id: str, payload: RoleUpdate):
        try:
            role_data = self.service.update_role(
                int(role_id), 
                name=payload.name, 
                description=payload.description
            )
            return role_data
        except BusinessException as e:
            return 400, {"message": str(e)}
        except Exception as e:
            return 400, {"message": str(e)}

    @http_delete("/{role_id}", response={204: None})
    def delete_role(self, role_id: str):
        try:
            self.service.delete_role(int(role_id))
            return 204, None
        except BusinessException as e:
            return 400, {"message": str(e)}
        except Exception as e:
            return 400, {"message": str(e)}