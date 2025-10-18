"""
登录日志仓储实现
"""

from app.domain.repositories.login_log_repository import LoginLogRepository
from app.domain.models.login_log import LoginLog
from django.core.exceptions import ObjectDoesNotExist
from typing import Optional, List, Union
from django.apps import apps
from .base_repository import BaseRepository


class DjangoORMLoginLogRepository(LoginLogRepository, BaseRepository[LoginLog]):
    def __init__(self):
        # 获取实际的 Django 模型类
        self.LoginLogModel = apps.get_model("domain", "LoginLog")
        # 初始化基类
        BaseRepository.__init__(self, self.LoginLogModel)

    def save(self, entity: LoginLog) -> None:
        entity.save()

    def find_by_id(self, entity_id: Union[int, str]) -> Optional[LoginLog]:
        try:
            # 如果传入的是整数，转换为字符串
            if isinstance(entity_id, int):
                entity_id = str(entity_id)
            return self.LoginLogModel.objects.get(pk=entity_id)
        except ObjectDoesNotExist:
            return None

    def delete(self, entity_id: Union[int, str]) -> bool:
        try:
            # 如果传入的是整数，转换为字符串
            if isinstance(entity_id, int):
                entity_id = str(entity_id)
            log = self.LoginLogModel.objects.get(pk=entity_id)
            log.delete()
            return True
        except ObjectDoesNotExist:
            return False

    def list_all(self) -> List[LoginLog]:
        return list(self.LoginLogModel.objects.all())