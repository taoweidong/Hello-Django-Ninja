"""
权限管理 API Controller
"""

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import Permission as DjangoPermission
from ninja_extra import api_controller, http_get, http_post, http_put, http_delete, permissions
from ninja_jwt.authentication import JWTAuth

from app.application.services.permission_service import PermissionService
from app.common.exceptions import BusinessException
from app.infrastructure.persistence.repos.permission_repo_impl import (
    DjangoORMPermissionRepository,
)
from app.api.schemas import PermissionOut, PermissionCreate, PermissionUpdate


@api_controller("/permissions", auth=JWTAuth())
class PermissionsController:
    def __init__(self):
        # 实例化仓储实现
        permission_repo = DjangoORMPermissionRepository()
        # 实例化应用服务
        self.service = PermissionService(permission_repo)

    @http_get("/{permission_id}", response=PermissionOut)
    def get_permission(self, permission_id: int):
        try:
            permission_data = self.service.get_permission_by_id(permission_id)
            return permission_data
        except BusinessException as e:
            return 400, {"message": str(e)}

    @http_get("/", response=list[PermissionOut])
    def list_permissions(self):
        # 实现列出所有权限的逻辑
        try:
            permissions = DjangoPermission.objects.all()
            return [
                PermissionOut(
                    id=perm.id,
                    name=perm.name,
                    codename=perm.codename
                )
                for perm in permissions
            ]
        except Exception as e:
            return 400, {"message": str(e)}

    @http_post("/", response={201: PermissionOut})
    def create_permission(self, payload: PermissionCreate):
        try:
            permission = DjangoPermission.objects.create(
                name=payload.name,
                codename=payload.codename,
                content_type_id=payload.content_type_id
            )
            return 201, PermissionOut(
                id=permission.id,
                name=permission.name,
                codename=permission.codename
            )
        except Exception as e:
            return 400, {"message": str(e)}

    @http_put("/{permission_id}", response=PermissionOut)
    def update_permission(self, permission_id: int, payload: PermissionUpdate):
        try:
            permission = DjangoPermission.objects.get(id=permission_id)
            if payload.name is not None:
                permission.name = payload.name
            if payload.codename is not None:
                permission.codename = payload.codename
            if payload.content_type_id is not None:
                permission.content_type_id = payload.content_type_id
            permission.save()
            return PermissionOut(
                id=permission.id,
                name=permission.name,
                codename=permission.codename
            )
        except ObjectDoesNotExist:
            return 404, {"message": "Permission not found"}
        except Exception as e:
            return 400, {"message": str(e)}

    @http_delete("/{permission_id}", response={204: None})
    def delete_permission(self, permission_id: int):
        try:
            permission = DjangoPermission.objects.get(id=permission_id)
            permission.delete()
            return 204, None
        except ObjectDoesNotExist:
            return 404, {"message": "Permission not found"}
        except Exception as e:
            return 400, {"message": str(e)}