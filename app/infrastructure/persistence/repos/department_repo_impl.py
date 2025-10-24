"""
部门仓储实现
"""

from app.domain.repositories.department_repository import DepartmentRepository
from app.domain.models.department import Department
from django.core.exceptions import ObjectDoesNotExist
from typing import Optional, List, Union
from django.apps import apps
from .base_repository import BaseRepository


class DjangoORMDepartmentRepository(DepartmentRepository, BaseRepository[Department]):
    def __init__(self):
        # 获取实际的 Django 模型类
        self.DepartmentModel = apps.get_model("domain", "Department")
        # 初始化基类
        BaseRepository.__init__(self, self.DepartmentModel)

    def save(self, entity: Department) -> None:
        entity.save()

    def find_by_id(self, entity_id: Union[int, str]) -> Optional[Department]:
        try:
            # 如果传入的是整数，转换为字符串
            if isinstance(entity_id, int):
                entity_id = str(entity_id)
            return self.DepartmentModel.objects.get(pk=entity_id)
        except ObjectDoesNotExist:
            return None

    def find_by_code(self, code: str) -> Optional[Department]:
        try:
            return self.DepartmentModel.objects.get(code=code)
        except ObjectDoesNotExist:
            return None

    def delete(self, entity_id: Union[int, str]) -> bool:
        try:
            # 如果传入的是整数，转换为字符串
            if isinstance(entity_id, int):
                entity_id = str(entity_id)
            department = self.DepartmentModel.objects.get(pk=entity_id)
            department.delete()
            return True
        except ObjectDoesNotExist:
            return False

    def list_all(self) -> List[Department]:
        return list(self.DepartmentModel.objects.all())
