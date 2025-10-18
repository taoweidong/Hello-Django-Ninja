"""
权限管理 API Controller
"""

from ninja_extra import api_controller, http_get, http_post, http_put, http_delete
from ninja_jwt.authentication import JWTAuth

from app.application.services.permission_service import PermissionService
from app.common.exception.exceptions import BusinessException
from app.infrastructure.persistence.repos.permission_repo_impl import (
    DjangoORMPermissionRepository,
)
from app.api.schemas import PermissionOut, PermissionCreate, PermissionUpdate, ApiResponse
from app.common.api_response import success, error


@api_controller("/permissions", auth=JWTAuth())
class PermissionsController:
    def __init__(self):
        # 实例化仓储实现
        permission_repo = DjangoORMPermissionRepository()
        # 实例化应用服务
        self.service = PermissionService(permission_repo)

    @http_get("/{permission_id}", response=ApiResponse[PermissionOut])
    def get_permission(self, permission_id: int):
        try:
            permission_data = self.service.get_permission_by_id(permission_id)
            return success(permission_data, "Permission retrieved successfully")
        except BusinessException as e:
            return error(str(e), 400)

    @http_get("/", response=ApiResponse[list[PermissionOut]])
    def list_permissions(self):
        # 通过service层获取所有权限数据
        try:
            permissions_data = self.service.list_permissions()
            return success(permissions_data, "Permissions retrieved successfully")
        except Exception as e:
            return error(str(e), 400)

    @http_post("/", response=ApiResponse[PermissionOut])
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
            return success(permission_data, "Permission created successfully", 201)
        except BusinessException as e:
            return error(str(e), 400)
        except Exception as e:
            return error(str(e), 400)

    @http_put("/{permission_id}", response=ApiResponse[PermissionOut])
    def update_permission(self, permission_id: int, payload: PermissionUpdate):
        try:
            # 注意：这里需要获取content_type，简化实现中使用默认值
            # 在实际应用中，应该根据payload.content_type_id获取对应的content_type对象
            content_type = None
            if payload.content_type_id is not None:
                from django.contrib.contenttypes.models import ContentType
                content_type = ContentType.objects.get_for_id(payload.content_type_id)
            
            # 只传递非空值进行更新
            update_kwargs = {}
            if payload.name is not None:
                update_kwargs['name'] = payload.name
            if payload.codename is not None:
                update_kwargs['codename'] = payload.codename
            if content_type is not None:
                update_kwargs['content_type'] = content_type
                
            permission_data = self.service.update_permission(
                permission_id=permission_id,
                **update_kwargs
            )
            return success(permission_data, "Permission updated successfully")
        except BusinessException as e:
            return error(str(e), 400)
        except Exception as e:
            return error(str(e), 400)

    @http_delete("/{permission_id}", response=ApiResponse[None])
    def delete_permission(self, permission_id: int):
        try:
            self.service.delete_permission(permission_id)
            return success(None, "Permission deleted successfully")
        except BusinessException as e:
            return error(str(e), 400)
        except Exception as e:
            return error(str(e), 400)