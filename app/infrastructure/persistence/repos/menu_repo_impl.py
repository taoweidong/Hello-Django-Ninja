"""
菜单仓储实现
"""

from app.domain.repositories.menu_repository import MenuRepository
from app.domain.models.menu import Menu
from django.core.exceptions import ObjectDoesNotExist
from typing import Optional, List, Union
from django.apps import apps
from .base_repository import BaseRepository


class DjangoORMMenuRepository(MenuRepository, BaseRepository[Menu]):
    def __init__(self):
        # 获取实际的 Django 模型类
        self.MenuModel = apps.get_model("domain", "Menu")
        # 初始化基类
        BaseRepository.__init__(self, self.MenuModel)

    def save(self, entity: Menu) -> None:
        entity.save()

    def find_by_id(self, entity_id: Union[int, str]) -> Optional[Menu]:
        try:
            # 如果传入的是整数，转换为字符串
            if isinstance(entity_id, int):
                entity_id = str(entity_id)
            return self.MenuModel.objects.get(pk=entity_id)
        except ObjectDoesNotExist:
            return None

    def find_by_name(self, name: str) -> Optional[Menu]:
        try:
            return self.MenuModel.objects.get(name=name)
        except ObjectDoesNotExist:
            return None

    def delete(self, entity_id: Union[int, str]) -> bool:
        try:
            # 如果传入的是整数，转换为字符串
            if isinstance(entity_id, int):
                entity_id = str(entity_id)
            menu = self.MenuModel.objects.get(pk=entity_id)
            menu.delete()
            return True
        except ObjectDoesNotExist:
            return False

    def list_all(self) -> List[Menu]:
        return list(self.MenuModel.objects.all())