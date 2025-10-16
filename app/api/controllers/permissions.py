"""
权限管理 API Controller
"""

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
        # 通过service层获取所有权限数据
        try:
            permissions_data = self.service.list_permissions()
            return permissions_data
        except Exception as e:
            return 400, {"message": str(e)}

    @http_post("/", response={201: PermissionOut})
    def create_permission(self, payload: PermissionCreate):
        try:
            # 注意：这里需要获取content_type，简化实现中使用默认值
            # 在实际应用中，应该根据payload.content_type_id获取对应的content_type对象
            from django.contrib.contenttypes.models import ContentType
            content_type = ContentType.objects.get_for_model(ContentType)  # 简化实现
            
            permission_data = self.service.create_permission(
                name=payload.name,
                codename=payload.codename,
                content_type=content_type
            )
            return 201, permission_data
        except BusinessException as e:
            return 400, {"message": str(e)}
        except Exception as e:
            return 400, {"message": str(e)}

    @http_put("/{permission_id}", response=PermissionOut)
    def update_permission(self, permission_id: int, payload: PermissionUpdate):
        try:
            # 注意：这里需要获取content_type，简化实现中使用默认值
            # 在实际应用中，应该根据payload.content_type_id获取对应的content_type对象
            content_type = None
            if payload.content_type_id is not None:
                from django.contrib.contenttypes.models import ContentType
                content_type = ContentType.objects.get_for_id(payload.content_type_id)
            
            permission_data = self.service.update_permission(
                permission_id=permission_id,
                name=payload.name,
                codename=payload.codename,
                content_type=content_type
            )
            return permission_data
        except BusinessException as e:
            return 400, {"message": str(e)}
        except Exception as e:
            return 400, {"message": str(e)}

    @http_delete("/{permission_id}", response={204: None})
    def delete_permission(self, permission_id: int):
        try:
            self.service.delete_permission(permission_id)
            return 204, None
        except BusinessException as e:
            return 400, {"message": str(e)}
        except Exception as e:
            return 400, {"message": str(e)}