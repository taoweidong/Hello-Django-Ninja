"""
菜单管理 API Controller
"""

from django.core.exceptions import ObjectDoesNotExist
from django.apps import apps
from ninja_extra import api_controller, http_get, http_post, http_put, http_delete, permissions
from ninja_jwt.authentication import JWTAuth

from app.api.schemas import MenuOut, MenuCreate, MenuUpdate


@api_controller("/menus", auth=JWTAuth())
class MenusController:
    def __init__(self):
        # 获取实际的 Django 模型类
        self.MenuModel = apps.get_model("domain", "Menu")

    @http_post("/", response={201: MenuOut})
    def create_menu(self, payload: MenuCreate):
        try:
            menu = self.MenuModel(
                menu_type=payload.menu_type,
                name=payload.name,
                rank=payload.rank,
                path=payload.path,
                component=payload.component,
                is_active=payload.is_active,
                method=payload.method,
                parent_id=payload.parent_id,
                meta_id=payload.meta_id
            )
            menu.save()
            return 201, menu
        except Exception as e:
            return 400, {"message": str(e)}

    @http_get("/{menu_id}", response=MenuOut)
    def get_menu(self, menu_id: str):
        try:
            menu = self.MenuModel.objects.get(id=menu_id)
            return menu
        except ObjectDoesNotExist:
            return 404, {"message": "Menu not found"}

    @http_get("/", response=list[MenuOut])
    def list_menus(self):
        menus = self.MenuModel.objects.all()
        return menus

    @http_put("/{menu_id}", response=MenuOut)
    def update_menu(self, menu_id: str, payload: MenuUpdate):
        try:
            menu = self.MenuModel.objects.get(id=menu_id)
            if payload.menu_type is not None:
                menu.menu_type = payload.menu_type
            if payload.name is not None:
                menu.name = payload.name
            if payload.rank is not None:
                menu.rank = payload.rank
            if payload.path is not None:
                menu.path = payload.path
            if payload.component is not None:
                menu.component = payload.component
            if payload.is_active is not None:
                menu.is_active = payload.is_active
            if payload.method is not None:
                menu.method = payload.method
            if payload.parent_id is not None:
                menu.parent_id = payload.parent_id
            if payload.meta_id is not None:
                menu.meta_id = payload.meta_id
            menu.save()
            return menu
        except ObjectDoesNotExist:
            return 404, {"message": "Menu not found"}
        except Exception as e:
            return 400, {"message": str(e)}

    @http_delete("/{menu_id}", response={204: None})
    def delete_menu(self, menu_id: str):
        try:
            menu = self.MenuModel.objects.get(id=menu_id)
            menu.delete()
            return 204, None
        except ObjectDoesNotExist:
            return 404, {"message": "Menu not found"}