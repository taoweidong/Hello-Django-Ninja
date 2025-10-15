"""
系统配置相关应用服务
"""

from app.domain.models.system_config import SystemConfig
from app.common.exceptions import BusinessException
from typing import List, Optional


class SystemConfigService:
    def __init__(self):
        pass

    def create_system_config(
        self,
        key: str,
        value: str,
        is_active: bool = True,
        access: bool = True,
        inherit: bool = True,
        description: Optional[str] = None
    ) -> dict:
        """
        创建系统配置
        """
        # 检查key是否已存在
        if SystemConfig.objects.filter(key=key).exists():
            raise BusinessException(f"SystemConfig with key '{key}' already exists.")
        
        config = SystemConfig(
            key=key,
            value=value,
            is_active=is_active,
            access=access,
            inherit=inherit,
            description=description
        )
        config.save()
        return self._system_config_to_dict(config)

    def get_system_config(self, config_id: str) -> dict:
        """
        根据ID获取系统配置
        """
        try:
            config = SystemConfig.objects.get(id=config_id)
            return self._system_config_to_dict(config)
        except SystemConfig.DoesNotExist:
            raise BusinessException(f"SystemConfig with id '{config_id}' not found.")

    def get_system_config_by_key(self, key: str) -> dict:
        """
        根据key获取系统配置
        """
        try:
            config = SystemConfig.objects.get(key=key)
            return self._system_config_to_dict(config)
        except SystemConfig.DoesNotExist:
            raise BusinessException(f"SystemConfig with key '{key}' not found.")

    def update_system_config(
        self,
        config_id: str,
        key: Optional[str] = None,
        value: Optional[str] = None,
        is_active: Optional[bool] = None,
        access: Optional[bool] = None,
        inherit: Optional[bool] = None,
        description: Optional[str] = None
    ) -> dict:
        """
        更新系统配置信息
        """
        try:
            config = SystemConfig.objects.get(id=config_id)
            
            if key is not None:
                # 检查key是否已存在（排除当前配置）
                if SystemConfig.objects.filter(key=key).exclude(id=config_id).exists():
                    raise BusinessException(f"SystemConfig with key '{key}' already exists.")
                config.key = key
            if value is not None:
                config.value = value
            if is_active is not None:
                config.is_active = is_active
            if access is not None:
                config.access = access
            if inherit is not None:
                config.inherit = inherit
            if description is not None:
                config.description = description
            
            config.save()
            return self._system_config_to_dict(config)
        except SystemConfig.DoesNotExist:
            raise BusinessException(f"SystemConfig with id '{config_id}' not found.")

    def delete_system_config(self, config_id: str) -> bool:
        """
        删除系统配置
        """
        try:
            config = SystemConfig.objects.get(id=config_id)
            config.delete()
            return True
        except SystemConfig.DoesNotExist:
            raise BusinessException(f"SystemConfig with id '{config_id}' not found.")

    def list_system_configs(self) -> List[dict]:
        """
        获取所有系统配置列表
        """
        configs = SystemConfig.objects.all()
        return [self._system_config_to_dict(config) for config in configs]

    def _system_config_to_dict(self, config: SystemConfig) -> dict:
        """
        将SystemConfig对象转换为字典
        """
        return {
            "id": config.id,
            "key": config.key,
            "value": config.value,
            "is_active": config.is_active,
            "access": config.access,
            "inherit": config.inherit,
            "description": config.description,
            "created_time": config.created_time,
            "updated_time": config.updated_time
        }