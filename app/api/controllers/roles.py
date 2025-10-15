"""
角色管理 API Controller
"""

from django.core.exceptions import ObjectDoesNotExist
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
        # 实现获取角色的逻辑
        try:
            from django.apps import apps
            RoleModel = apps.get_model("domain", "Role")
            role = RoleModel.objects.get(id=role_id)
            return RoleOut(
                id=role.id,
                name=role.name,
                description=role.description
            )
        except ObjectDoesNotExist:
            return 404, {"message": "Role not found"}
        except Exception as e:
            return 400, {"message": str(e)}

    @http_get("/", response=list[RoleOut])
    def list_roles(self):
        # 实现列出所有角色的逻辑
        try:
            from django.apps import apps
            RoleModel = apps.get_model("domain", "Role")
            roles = RoleModel.objects.all()
            return [
                RoleOut(
                    id=role.id,
                    name=role.name,
                    description=role.description
                )
                for role in roles
            ]
        except Exception as e:
            return 400, {"message": str(e)}

    @http_put("/{role_id}", response=RoleOut)
    def update_role(self, role_id: str, payload: RoleUpdate):
        try:
            from django.apps import apps
            RoleModel = apps.get_model("domain", "Role")
            role = RoleModel.objects.get(id=role_id)
            if payload.name is not None:
                role.name = payload.name
            if payload.description is not None:
                role.description = payload.description
            role.save()
            return RoleOut(
                id=role.id,
                name=role.name,
                description=role.description
            )
        except ObjectDoesNotExist:
            return 404, {"message": "Role not found"}
        except Exception as e:
            return 400, {"message": str(e)}

    @http_delete("/{role_id}", response={204: None})
    def delete_role(self, role_id: str):
        try:
            from django.apps import apps
            RoleModel = apps.get_model("domain", "Role")
            role = RoleModel.objects.get(id=role_id)
            role.delete()
            return 204, None
        except ObjectDoesNotExist:
            return 404, {"message": "Role not found"}
        except Exception as e:
            return 400, {"message": str(e)}