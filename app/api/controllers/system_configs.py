"""
系统配置管理 API Controller
"""

from django.core.exceptions import ObjectDoesNotExist
from django.apps import apps
from ninja_extra import api_controller, http_get, http_post, http_put, http_delete, permissions
from ninja_jwt.authentication import JWTAuth

from app.api.schemas import SystemConfigOut, SystemConfigCreate, SystemConfigUpdate


@api_controller("/system-configs", auth=JWTAuth())
class SystemConfigsController:
    def __init__(self):
        # 获取实际的 Django 模型类
        self.SystemConfigModel = apps.get_model("domain", "SystemConfig")

    @http_post("/", response={201: SystemConfigOut})
    def create_system_config(self, payload: SystemConfigCreate):
        try:
            system_config = self.SystemConfigModel(
                key=payload.key,
                value=payload.value,
                description=payload.description,
                is_active=payload.is_active,
                access=payload.access,
                inherit=payload.inherit
            )
            system_config.save()
            return 201, system_config
        except Exception as e:
            return 400, {"message": str(e)}

    @http_get("/{config_id}", response=SystemConfigOut)
    def get_system_config(self, config_id: str):
        try:
            system_config = self.SystemConfigModel.objects.get(id=config_id)
            return system_config
        except ObjectDoesNotExist:
            return 404, {"message": "SystemConfig not found"}

    @http_get("/", response=list[SystemConfigOut])
    def list_system_configs(self):
        system_configs = self.SystemConfigModel.objects.all()
        return system_configs

    @http_put("/{config_id}", response=SystemConfigOut)
    def update_system_config(self, config_id: str, payload: SystemConfigUpdate):
        try:
            system_config = self.SystemConfigModel.objects.get(id=config_id)
            if payload.key is not None:
                system_config.key = payload.key
            if payload.value is not None:
                system_config.value = payload.value
            if payload.description is not None:
                system_config.description = payload.description
            if payload.is_active is not None:
                system_config.is_active = payload.is_active
            if payload.access is not None:
                system_config.access = payload.access
            if payload.inherit is not None:
                system_config.inherit = payload.inherit
            system_config.save()
            return system_config
        except ObjectDoesNotExist:
            return 404, {"message": "SystemConfig not found"}
        except Exception as e:
            return 400, {"message": str(e)}

    @http_delete("/{config_id}", response={204: None})
    def delete_system_config(self, config_id: str):
        try:
            system_config = self.SystemConfigModel.objects.get(id=config_id)
            system_config.delete()
            return 204, None
        except ObjectDoesNotExist:
            return 404, {"message": "SystemConfig not found"}