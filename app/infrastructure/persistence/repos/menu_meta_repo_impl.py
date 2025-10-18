"""
菜单元数据仓储实现
"""

from app.domain.repositories.menu_meta_repository import MenuMetaRepository
from app.domain.models.menu_meta import MenuMeta
from django.core.exceptions import ObjectDoesNotExist
from typing import Optional, List, Union
from django.apps import apps
from .base_repository import BaseRepository


class DjangoORMMenuMetaRepository(MenuMetaRepository, BaseRepository[MenuMeta]):
    def __init__(self):
        # 获取实际的 Django 模型类
        self.MenuMetaModel = apps.get_model("domain", "MenuMeta")
        # 初始化基类
        BaseRepository.__init__(self, self.MenuMetaModel)

    def save(self, entity: MenuMeta) -> None:
        entity.save()

    def find_by_id(self, entity_id: Union[int, str]) -> Optional[MenuMeta]:
        try:
            # 如果传入的是整数，转换为字符串
            if isinstance(entity_id, int):
                entity_id = str(entity_id)
            return self.MenuMetaModel.objects.get(pk=entity_id)
        except ObjectDoesNotExist:
            return None

    def delete(self, entity_id: Union[int, str]) -> bool:
        try:
            # 如果传入的是整数，转换为字符串
            if isinstance(entity_id, int):
                entity_id = str(entity_id)
            meta = self.MenuMetaModel.objects.get(pk=entity_id)
            meta.delete()
            return True
        except ObjectDoesNotExist:
            return False

    def list_all(self) -> List[MenuMeta]:
        return list(self.MenuMetaModel.objects.all())