"""
操作日志仓储实现
"""

from app.domain.repositories.operation_log_repository import OperationLogRepository
from app.domain.models.operation_log import OperationLog
from django.core.exceptions import ObjectDoesNotExist
from typing import Optional, List, Union
from django.apps import apps
from .base_repository import BaseRepository


class DjangoORMOperationLogRepository(OperationLogRepository, BaseRepository[OperationLog]):
    def __init__(self):
        # 获取实际的 Django 模型类
        self.OperationLogModel = apps.get_model("domain", "OperationLog")
        # 初始化基类
        BaseRepository.__init__(self, self.OperationLogModel)

    def save(self, entity: OperationLog) -> None:
        entity.save()

    def find_by_id(self, entity_id: Union[int, str]) -> Optional[OperationLog]:
        try:
            # 如果传入的是整数，转换为字符串
            if isinstance(entity_id, int):
                entity_id = str(entity_id)
            return self.OperationLogModel.objects.get(pk=entity_id)
        except ObjectDoesNotExist:
            return None

    def delete(self, entity_id: Union[int, str]) -> bool:
        try:
            # 如果传入的是整数，转换为字符串
            if isinstance(entity_id, int):
                entity_id = str(entity_id)
            log = self.OperationLogModel.objects.get(pk=entity_id)
            log.delete()
            return True
        except ObjectDoesNotExist:
            return False

    def list_all(self) -> List[OperationLog]:
        return list(self.OperationLogModel.objects.all())