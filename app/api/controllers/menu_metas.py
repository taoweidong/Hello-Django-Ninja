"""
菜单元数据管理 API Controller
"""

from django.core.exceptions import ObjectDoesNotExist
from django.apps import apps
from ninja_extra import api_controller, http_get, http_post, http_put, http_delete, permissions
from ninja_jwt.authentication import JWTAuth

from app.api.schemas import MenuMetaOut, MenuMetaCreate, MenuMetaUpdate


@api_controller("/menu-metas", auth=JWTAuth())
class MenuMetasController:
    def __init__(self):
        # 获取实际的 Django 模型类
        self.MenuMetaModel = apps.get_model("domain", "MenuMeta")

    @http_post("/", response={201: MenuMetaOut})
    def create_menu_meta(self, payload: MenuMetaCreate):
        try:
            menu_meta = self.MenuMetaModel(
                title=payload.title,
                icon=payload.icon,
                r_svg_name=payload.r_svg_name,
                is_show_menu=payload.is_show_menu,
                is_show_parent=payload.is_show_parent,
                is_keepalive=payload.is_keepalive,
                frame_url=payload.frame_url,
                frame_loading=payload.frame_loading,
                transition_enter=payload.transition_enter,
                transition_leave=payload.transition_leave,
                is_hidden_tag=payload.is_hidden_tag,
                fixed_tag=payload.fixed_tag,
                dynamic_level=payload.dynamic_level
            )
            menu_meta.save()
            return 201, menu_meta
        except Exception as e:
            return 400, {"message": str(e)}

    @http_get("/{menu_meta_id}", response=MenuMetaOut)
    def get_menu_meta(self, menu_meta_id: str):
        try:
            menu_meta = self.MenuMetaModel.objects.get(id=menu_meta_id)
            return menu_meta
        except ObjectDoesNotExist:
            return 404, {"message": "MenuMeta not found"}

    @http_get("/", response=list[MenuMetaOut])
    def list_menu_metas(self):
        menu_metas = self.MenuMetaModel.objects.all()
        return menu_metas

    @http_put("/{menu_meta_id}", response=MenuMetaOut)
    def update_menu_meta(self, menu_meta_id: str, payload: MenuMetaUpdate):
        try:
            menu_meta = self.MenuMetaModel.objects.get(id=menu_meta_id)
            if payload.title is not None:
                menu_meta.title = payload.title
            if payload.icon is not None:
                menu_meta.icon = payload.icon
            if payload.r_svg_name is not None:
                menu_meta.r_svg_name = payload.r_svg_name
            if payload.is_show_menu is not None:
                menu_meta.is_show_menu = payload.is_show_menu
            if payload.is_show_parent is not None:
                menu_meta.is_show_parent = payload.is_show_parent
            if payload.is_keepalive is not None:
                menu_meta.is_keepalive = payload.is_keepalive
            if payload.frame_url is not None:
                menu_meta.frame_url = payload.frame_url
            if payload.frame_loading is not None:
                menu_meta.frame_loading = payload.frame_loading
            if payload.transition_enter is not None:
                menu_meta.transition_enter = payload.transition_enter
            if payload.transition_leave is not None:
                menu_meta.transition_leave = payload.transition_leave
            if payload.is_hidden_tag is not None:
                menu_meta.is_hidden_tag = payload.is_hidden_tag
            if payload.fixed_tag is not None:
                menu_meta.fixed_tag = payload.fixed_tag
            if payload.dynamic_level is not None:
                menu_meta.dynamic_level = payload.dynamic_level
            menu_meta.save()
            return menu_meta
        except ObjectDoesNotExist:
            return 404, {"message": "MenuMeta not found"}
        except Exception as e:
            return 400, {"message": str(e)}

    @http_delete("/{menu_meta_id}", response={204: None})
    def delete_menu_meta(self, menu_meta_id: str):
        try:
            menu_meta = self.MenuMetaModel.objects.get(id=menu_meta_id)
            menu_meta.delete()
            return 204, None
        except ObjectDoesNotExist:
            return 404, {"message": "MenuMeta not found"}