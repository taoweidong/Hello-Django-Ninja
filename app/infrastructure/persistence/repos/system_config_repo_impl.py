"""
系统配置仓储实现
"""

from app.domain.repositories.system_config_repository import SystemConfigRepository
from app.domain.models.system_config import SystemConfig
from django.core.exceptions import ObjectDoesNotExist
from typing import Optional, List, Union
from django.apps import apps
from .base_repository import BaseRepository


class DjangoORMSystemConfigRepository(SystemConfigRepository, BaseRepository[SystemConfig]):
    def __init__(self):
        # 获取实际的 Django 模型类
        self.SystemConfigModel = apps.get_model("domain", "SystemConfig")
        # 初始化基类
        BaseRepository.__init__(self, self.SystemConfigModel)

    def save(self, entity: SystemConfig) -> None:
        entity.save()

    def find_by_id(self, entity_id: Union[int, str]) -> Optional[SystemConfig]:
        try:
            # 如果传入的是整数，转换为字符串
            if isinstance(entity_id, int):
                entity_id = str(entity_id)
            return self.SystemConfigModel.objects.get(pk=entity_id)
        except ObjectDoesNotExist:
            return None

    def find_by_key(self, key: str) -> Optional[SystemConfig]:
        try:
            return self.SystemConfigModel.objects.get(key=key)
        except ObjectDoesNotExist:
            return None

    def delete(self, entity_id: Union[int, str]) -> bool:
        try:
            # 如果传入的是整数，转换为字符串
            if isinstance(entity_id, int):
                entity_id = str(entity_id)
            config = self.SystemConfigModel.objects.get(pk=entity_id)
            config.delete()
            return True
        except ObjectDoesNotExist:
            return False

    def list_all(self) -> List[SystemConfig]:
        return list(self.SystemConfigModel.objects.all())