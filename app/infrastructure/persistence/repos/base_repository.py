"""
基础仓储类，封装通用的CRUD操作
"""

from django.core.exceptions import ObjectDoesNotExist
from typing import TypeVar, Generic, Optional, List, Type

T = TypeVar('T')  # 泛型类型变量，代表模型类


class BaseRepository(Generic[T]):
    def __init__(self, model_class: Type[T]):
        """
        初始化基础仓储
        
        Args:
            model_class: Django模型类
        """
        self.model_class = model_class

    def save(self, entity: T) -> None:
        """
        保存实体
        
        Args:
            entity: 要保存的实体对象
        """
        entity.save()

    def find_by_id(self, entity_id: int) -> Optional[T]:
        """
        根据ID查找实体
        
        Args:
            entity_id: 实体ID
            
        Returns:
            实体对象或None
        """
        try:
            return self.model_class.objects.get(pk=entity_id)
        except ObjectDoesNotExist:
            return None

    def delete(self, entity_id: int) -> bool:
        """
        根据ID删除实体
        
        Args:
            entity_id: 实体ID
            
        Returns:
            删除成功返回True，否则返回False
        """
        try:
            entity = self.model_class.objects.get(pk=entity_id)
            entity.delete()
            return True
        except ObjectDoesNotExist:
            return False

    def list_all(self) -> List[T]:
        """
        获取所有实体列表
        
        Returns:
            实体对象列表
        """
        return list(self.model_class.objects.all())