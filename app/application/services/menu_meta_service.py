"""
菜单元数据相关应用服务
"""

from app.domain.models.menu_meta import MenuMeta
from app.common.exceptions import BusinessException
from typing import List, Optional


class MenuMetaService:
    def __init__(self):
        pass

    def create_menu_meta(
        self,
        title: Optional[str] = None,
        icon: Optional[str] = None,
        r_svg_name: Optional[str] = None,
        is_show_menu: bool = True,
        is_show_parent: bool = True,
        is_keepalive: bool = True,
        frame_url: Optional[str] = None,
        frame_loading: bool = False,
        transition_enter: Optional[str] = None,
        transition_leave: Optional[str] = None,
        is_hidden_tag: bool = False,
        fixed_tag: bool = False,
        dynamic_level: int = 0
    ) -> dict:
        """
        创建菜单元数据
        """
        menu_meta = MenuMeta(
            title=title,
            icon=icon,
            r_svg_name=r_svg_name,
            is_show_menu=is_show_menu,
            is_show_parent=is_show_parent,
            is_keepalive=is_keepalive,
            frame_url=frame_url,
            frame_loading=frame_loading,
            transition_enter=transition_enter,
            transition_leave=transition_leave,
            is_hidden_tag=is_hidden_tag,
            fixed_tag=fixed_tag,
            dynamic_level=dynamic_level
        )
        menu_meta.save()
        return self._menu_meta_to_dict(menu_meta)

    def get_menu_meta(self, menu_meta_id: str) -> dict:
        """
        根据ID获取菜单元数据
        """
        try:
            menu_meta = MenuMeta.objects.get(id=menu_meta_id)
            return self._menu_meta_to_dict(menu_meta)
        except MenuMeta.DoesNotExist:
            raise BusinessException(f"MenuMeta with id '{menu_meta_id}' not found.")

    def update_menu_meta(
        self,
        menu_meta_id: str,
        title: Optional[str] = None,
        icon: Optional[str] = None,
        r_svg_name: Optional[str] = None,
        is_show_menu: Optional[bool] = None,
        is_show_parent: Optional[bool] = None,
        is_keepalive: Optional[bool] = None,
        frame_url: Optional[str] = None,
        frame_loading: Optional[bool] = None,
        transition_enter: Optional[str] = None,
        transition_leave: Optional[str] = None,
        is_hidden_tag: Optional[bool] = None,
        fixed_tag: Optional[bool] = None,
        dynamic_level: Optional[int] = None
    ) -> dict:
        """
        更新菜单元数据信息
        """
        try:
            menu_meta = MenuMeta.objects.get(id=menu_meta_id)
            
            if title is not None:
                menu_meta.title = title
            if icon is not None:
                menu_meta.icon = icon
            if r_svg_name is not None:
                menu_meta.r_svg_name = r_svg_name
            if is_show_menu is not None:
                menu_meta.is_show_menu = is_show_menu
            if is_show_parent is not None:
                menu_meta.is_show_parent = is_show_parent
            if is_keepalive is not None:
                menu_meta.is_keepalive = is_keepalive
            if frame_url is not None:
                menu_meta.frame_url = frame_url
            if frame_loading is not None:
                menu_meta.frame_loading = frame_loading
            if transition_enter is not None:
                menu_meta.transition_enter = transition_enter
            if transition_leave is not None:
                menu_meta.transition_leave = transition_leave
            if is_hidden_tag is not None:
                menu_meta.is_hidden_tag = is_hidden_tag
            if fixed_tag is not None:
                menu_meta.fixed_tag = fixed_tag
            if dynamic_level is not None:
                menu_meta.dynamic_level = dynamic_level
            
            menu_meta.save()
            return self._menu_meta_to_dict(menu_meta)
        except MenuMeta.DoesNotExist:
            raise BusinessException(f"MenuMeta with id '{menu_meta_id}' not found.")

    def delete_menu_meta(self, menu_meta_id: str) -> bool:
        """
        删除菜单元数据
        """
        try:
            menu_meta = MenuMeta.objects.get(id=menu_meta_id)
            menu_meta.delete()
            return True
        except MenuMeta.DoesNotExist:
            raise BusinessException(f"MenuMeta with id '{menu_meta_id}' not found.")

    def list_menu_metas(self) -> List[dict]:
        """
        获取所有菜单元数据列表
        """
        menu_metas = MenuMeta.objects.all()
        return [self._menu_meta_to_dict(meta) for meta in menu_metas]

    def _menu_meta_to_dict(self, menu_meta: MenuMeta) -> dict:
        """
        将MenuMeta对象转换为字典
        """
        return {
            "id": menu_meta.id,
            "title": menu_meta.title,
            "icon": menu_meta.icon,
            "r_svg_name": menu_meta.r_svg_name,
            "is_show_menu": menu_meta.is_show_menu,
            "is_show_parent": menu_meta.is_show_parent,
            "is_keepalive": menu_meta.is_keepalive,
            "frame_url": menu_meta.frame_url,
            "frame_loading": menu_meta.frame_loading,
            "transition_enter": menu_meta.transition_enter,
            "transition_leave": menu_meta.transition_leave,
            "is_hidden_tag": menu_meta.is_hidden_tag,
            "fixed_tag": menu_meta.fixed_tag,
            "dynamic_level": menu_meta.dynamic_level,
            "created_time": menu_meta.created_time,
            "updated_time": menu_meta.updated_time
        }