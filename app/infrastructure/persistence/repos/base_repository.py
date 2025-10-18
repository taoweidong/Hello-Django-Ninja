"""
基础仓储类，封装通用的CRUD操作
"""

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import QuerySet
from typing import TypeVar, Generic, Optional, List, Type, Union, Dict, Any

# 定义一个绑定到Django模型的泛型类型变量
T = TypeVar('T', bound=models.Model)  # 泛型类型变量，代表Django模型类


class BaseRepository(Generic[T]):
    model_class: Type[T]
    
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

    def find_by_id(self, entity_id: Union[int, str]) -> Optional[T]:
        """
        根据ID查找实体
        
        Args:
            entity_id: 实体ID
            
        Returns:
            实体对象或None
        """
        try:
            # 如果传入的是整数，转换为字符串
            if isinstance(entity_id, int):
                entity_id = str(entity_id)
            return self.model_class.objects.get(pk=entity_id)  # type: ignore
        except ObjectDoesNotExist:
            return None

    def delete(self, entity_id: Union[int, str]) -> bool:
        """
        根据ID删除实体
        
        Args:
            entity_id: 实体ID
            
        Returns:
            删除成功返回True，否则返回False
        """
        try:
            # 如果传入的是整数，转换为字符串
            if isinstance(entity_id, int):
                entity_id = str(entity_id)
            entity = self.model_class.objects.get(pk=entity_id)  # type: ignore
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
        return list(self.model_class.objects.all())  # type: ignore
    
    def list_with_pagination(
        self, 
        page: int = 1, 
        page_size: int = 20,
        filters: Optional[Dict[str, Any]] = None,
        order_by: Optional[List[str]] = None,
        search: Optional[str] = None,
        search_fields: Optional[List[str]] = None
    ) -> QuerySet[T]:
        """
        获取实体列表，支持分页、过滤、排序和搜索功能
        
        Args:
            page: 页码，默认为1
            page_size: 每页数量，默认为20
            filters: 过滤条件字典
            order_by: 排序字段列表
            search: 搜索关键字
            search_fields: 搜索字段列表
            
        Returns:
            分页后的查询集
        """
        queryset = self.model_class.objects.all()  # type: ignore
        
        # 应用过滤条件
        if filters:
            queryset = queryset.filter(**filters)
        
        # 应用搜索条件
        if search and search_fields:
            # 构建搜索条件
            search_filters = {}
            for field in search_fields:
                search_filters[f"{field}__icontains"] = search
            queryset = queryset.filter(**search_filters)
        
        # 应用排序
        if order_by:
            queryset = queryset.order_by(*order_by)
            
        return queryset