"""
菜单相关应用服务
"""

from app.domain.models.menu import Menu
from app.domain.models.menu_meta import MenuMeta
from app.common.exception.exceptions import BusinessException
from typing import List, Optional


class MenuService:
    def __init__(self):
        pass

    def create_menu(
        self,
        menu_type: int,
        name: str,
        rank: int = 0,
        path: Optional[str] = None,
        component: Optional[str] = None,
        is_active: bool = True,
        method: Optional[str] = None,
        parent_id: Optional[str] = None,
        meta_id: Optional[str] = None
    ) -> dict:
        """
        创建菜单
        """
        # 检查name是否已存在
        if Menu.objects.filter(name=name).exists():
            raise BusinessException(f"Menu with name '{name}' already exists.")
        
        # 检查meta_id是否存在
        if meta_id:
            try:
                meta = MenuMeta.objects.get(id=meta_id)
            except MenuMeta.DoesNotExist:
                raise BusinessException(f"MenuMeta with id '{meta_id}' not found.")
        
        menu = Menu(
            menu_type=menu_type,
            name=name,
            rank=rank,
            path=path,
            component=component,
            is_active=is_active,
            method=method,
            parent_id=parent_id,
            meta_id=meta_id
        )
        menu.save()
        return self._menu_to_dict(menu)

    def get_menu(self, menu_id: str) -> dict:
        """
        根据ID获取菜单
        """
        try:
            menu = Menu.objects.get(id=menu_id)
            return self._menu_to_dict(menu)
        except Menu.DoesNotExist:
            raise BusinessException(f"Menu with id '{menu_id}' not found.")

    def update_menu(
        self,
        menu_id: str,
        menu_type: Optional[int] = None,
        name: Optional[str] = None,
        rank: Optional[int] = None,
        path: Optional[str] = None,
        component: Optional[str] = None,
        is_active: Optional[bool] = None,
        method: Optional[str] = None,
        parent_id: Optional[str] = None,
        meta_id: Optional[str] = None
    ) -> dict:
        """
        更新菜单信息
        """
        try:
            menu = Menu.objects.get(id=menu_id)
            
            if menu_type is not None:
                menu.menu_type = menu_type
            if name is not None:
                # 检查name是否已存在（排除当前菜单）
                if Menu.objects.filter(name=name).exclude(id=menu_id).exists():
                    raise BusinessException(f"Menu with name '{name}' already exists.")
                menu.name = name
            if rank is not None:
                menu.rank = rank
            if path is not None:
                menu.path = path
            if component is not None:
                menu.component = component
            if is_active is not None:
                menu.is_active = is_active
            if method is not None:
                menu.method = method
            if parent_id is not None:
                menu.parent_id = parent_id
            if meta_id is not None:
                # 检查meta_id是否存在
                try:
                    meta = MenuMeta.objects.get(id=meta_id)
                except MenuMeta.DoesNotExist:
                    raise BusinessException(f"MenuMeta with id '{meta_id}' not found.")
                menu.meta_id = meta_id
            
            menu.save()
            return self._menu_to_dict(menu)
        except Menu.DoesNotExist:
            raise BusinessException(f"Menu with id '{menu_id}' not found.")

    def delete_menu(self, menu_id: str) -> bool:
        """
        删除菜单
        """
        try:
            menu = Menu.objects.get(id=menu_id)
            menu.delete()
            return True
        except Menu.DoesNotExist:
            raise BusinessException(f"Menu with id '{menu_id}' not found.")

    def list_menus(self) -> List[dict]:
        """
        获取所有菜单列表
        """
        menus = Menu.objects.all()
        return [self._menu_to_dict(menu) for menu in menus]

    def _menu_to_dict(self, menu: Menu) -> dict:
        """
        将Menu对象转换为字典
        """
        return {
            "id": menu.id,
            "menu_type": menu.menu_type,
            "name": menu.name,
            "rank": menu.rank,
            "path": menu.path,
            "component": menu.component,
            "is_active": menu.is_active,
            "method": menu.method,
            "parent_id": menu.parent_id,
            "meta_id": menu.meta_id,
            "created_time": menu.created_time,
            "updated_time": menu.updated_time
        }