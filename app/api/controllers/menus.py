"""
菜单管理 API Controller
"""

from ninja_extra import api_controller, http_get, http_post, http_put, http_delete
from ninja_jwt.authentication import JWTAuth

from app.application.services.menu_service import MenuService
from app.common.exception.exceptions import BusinessException
from app.api.schemas import MenuOut, MenuCreate, MenuUpdate


@api_controller("/menus", auth=JWTAuth())
class MenusController:
    def __init__(self):
        # 实例化应用服务
        self.service = MenuService()

    @http_post("/", response={201: MenuOut})
    def create_menu(self, payload: MenuCreate):
        try:
            menu_data = self.service.create_menu(
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
            return 201, menu_data
        except BusinessException as e:
            return 400, {"message": str(e)}
        except Exception as e:
            return 400, {"message": str(e)}

    @http_get("/{menu_id}", response=MenuOut)
    def get_menu(self, menu_id: str):
        try:
            menu_data = self.service.get_menu(menu_id)
            return menu_data
        except BusinessException as e:
            return 400, {"message": str(e)}
        except Exception as e:
            return 400, {"message": str(e)}

    @http_get("/", response=list[MenuOut])
    def list_menus(self):
        try:
            menus_data = self.service.list_menus()
            return menus_data
        except Exception as e:
            return 400, {"message": str(e)}

    @http_put("/{menu_id}", response=MenuOut)
    def update_menu(self, menu_id: str, payload: MenuUpdate):
        try:
            menu_data = self.service.update_menu(
                menu_id=menu_id,
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
            return menu_data
        except BusinessException as e:
            return 400, {"message": str(e)}
        except Exception as e:
            return 400, {"message": str(e)}

    @http_delete("/{menu_id}", response={204: None})
    def delete_menu(self, menu_id: str):
        try:
            self.service.delete_menu(menu_id)
            return 204, None
        except BusinessException as e:
            return 400, {"message": str(e)}
        except Exception as e:
            return 400, {"message": str(e)}