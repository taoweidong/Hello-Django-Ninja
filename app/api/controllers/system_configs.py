"""
系统配置管理 API Controller
"""

from ninja_extra import api_controller, http_get, http_post, http_put, http_delete
from ninja_jwt.authentication import JWTAuth

from app.application.services.system_config_service import SystemConfigService
from app.common.exception.exceptions import BusinessException
from app.api.schemas import SystemConfigOut, SystemConfigCreate, SystemConfigUpdate, ApiResponse
from app.common.api_response import success, error


@api_controller("/system-configs", auth=JWTAuth())
class SystemConfigsController:
    def __init__(self):
        # 实例化应用服务
        self.service = SystemConfigService()

    @http_post("/", response=ApiResponse[SystemConfigOut])
    def create_system_config(self, payload: SystemConfigCreate):
        try:
            config_data = self.service.create_system_config(
                key=payload.key,
                value=payload.value,
                description=payload.description,
                is_active=payload.is_active,
                access=payload.access,
                inherit=payload.inherit
            )
            return success(config_data, "System config created successfully", 201)
        except BusinessException as e:
            return error(str(e), 400)
        except Exception as e:
            return error(str(e), 400)

    @http_get("/{config_id}", response=ApiResponse[SystemConfigOut])
    def get_system_config(self, config_id: str):
        try:
            config_data = self.service.get_system_config(config_id)
            return success(config_data, "System config retrieved successfully")
        except BusinessException as e:
            return error(str(e), 400)
        except Exception as e:
            return error(str(e), 400)

    @http_get("/", response=ApiResponse[list[SystemConfigOut]])
    def list_system_configs(self):
        try:
            configs_data = self.service.list_system_configs()
            return success(configs_data, "System configs retrieved successfully")
        except Exception as e:
            return error(str(e), 400)

    @http_put("/{config_id}", response=ApiResponse[SystemConfigOut])
    def update_system_config(self, config_id: str, payload: SystemConfigUpdate):
        try:
            # 只传递非空值进行更新
            update_kwargs = {}
            if payload.key is not None:
                update_kwargs['key'] = payload.key
            if payload.value is not None:
                update_kwargs['value'] = payload.value
            if payload.description is not None:
                update_kwargs['description'] = payload.description
            if payload.is_active is not None:
                update_kwargs['is_active'] = payload.is_active
            if payload.access is not None:
                update_kwargs['access'] = payload.access
            if payload.inherit is not None:
                update_kwargs['inherit'] = payload.inherit
                
            config_data = self.service.update_system_config(
                config_id=config_id,
                **update_kwargs
            )
            return success(config_data, "System config updated successfully")
        except BusinessException as e:
            return error(str(e), 400)
        except Exception as e:
            return error(str(e), 400)

    @http_delete("/{config_id}", response=ApiResponse[None])
    def delete_system_config(self, config_id: str):
        try:
            self.service.delete_system_config(config_id)
            return success(None, "System config deleted successfully")
        except BusinessException as e:
            return error(str(e), 400)
        except Exception as e:
            return error(str(e), 400)