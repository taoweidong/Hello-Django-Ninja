"""
系统配置管理 API Controller
"""

from ninja_extra import api_controller, http_get, http_post, http_put, http_delete, permissions
from ninja_jwt.authentication import JWTAuth

from app.application.services.system_config_service import SystemConfigService
from app.common.exceptions import BusinessException
from app.api.schemas import SystemConfigOut, SystemConfigCreate, SystemConfigUpdate


@api_controller("/system-configs", auth=JWTAuth())
class SystemConfigsController:
    def __init__(self):
        # 实例化应用服务
        self.service = SystemConfigService()

    @http_post("/", response={201: SystemConfigOut})
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
            return 201, config_data
        except BusinessException as e:
            return 400, {"message": str(e)}
        except Exception as e:
            return 400, {"message": str(e)}

    @http_get("/{config_id}", response=SystemConfigOut)
    def get_system_config(self, config_id: str):
        try:
            config_data = self.service.get_system_config(config_id)
            return config_data
        except BusinessException as e:
            return 400, {"message": str(e)}
        except Exception as e:
            return 400, {"message": str(e)}

    @http_get("/", response=list[SystemConfigOut])
    def list_system_configs(self):
        try:
            configs_data = self.service.list_system_configs()
            return configs_data
        except Exception as e:
            return 400, {"message": str(e)}

    @http_put("/{config_id}", response=SystemConfigOut)
    def update_system_config(self, config_id: str, payload: SystemConfigUpdate):
        try:
            config_data = self.service.update_system_config(
                config_id=config_id,
                key=payload.key,
                value=payload.value,
                description=payload.description,
                is_active=payload.is_active,
                access=payload.access,
                inherit=payload.inherit
            )
            return config_data
        except BusinessException as e:
            return 400, {"message": str(e)}
        except Exception as e:
            return 400, {"message": str(e)}

    @http_delete("/{config_id}", response={204: None})
    def delete_system_config(self, config_id: str):
        try:
            self.service.delete_system_config(config_id)
            return 204, None
        except BusinessException as e:
            return 400, {"message": str(e)}
        except Exception as e:
            return 400, {"message": str(e)}