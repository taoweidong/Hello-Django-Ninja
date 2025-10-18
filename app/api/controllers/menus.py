"""
菜单管理 API Controller
"""

from ninja_extra import api_controller, http_get, http_post, http_put, http_delete
from ninja_jwt.authentication import JWTAuth

from app.application.services.menu_service import MenuService
from app.common.exception.exceptions import BusinessException
from app.api.schemas import MenuOut, MenuCreate, MenuUpdate, ApiResponse
from app.common.api_response import success, error


@api_controller("/menus", auth=JWTAuth())
class MenusController:
    def __init__(self):
        # 实例化应用服务
        self.service = MenuService()

    @http_post("/", response=ApiResponse[MenuOut])
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
            return success(menu_data, "Menu created successfully", 201)
        except BusinessException as e:
            return error(str(e), 400)
        except Exception as e:
            return error(str(e), 400)

    @http_get("/{menu_id}", response=ApiResponse[MenuOut])
    def get_menu(self, menu_id: str):
        try:
            menu_data = self.service.get_menu(menu_id)
            return success(menu_data, "Menu retrieved successfully")
        except BusinessException as e:
            return error(str(e), 400)
        except Exception as e:
            return error(str(e), 400)

    @http_get("/", response=ApiResponse[list[MenuOut]])
    def list_menus(self):
        try:
            menus_data = self.service.list_menus()
            return success(menus_data, "Menus retrieved successfully")
        except Exception as e:
            return error(str(e), 400)

    @http_put("/{menu_id}", response=ApiResponse[MenuOut])
    def update_menu(self, menu_id: str, payload: MenuUpdate):
        try:
            # 只传递非空值进行更新
            update_kwargs = {}
            if payload.menu_type is not None:
                update_kwargs['menu_type'] = payload.menu_type
            if payload.name is not None:
                update_kwargs['name'] = payload.name
            if payload.rank is not None:
                update_kwargs['rank'] = payload.rank
            if payload.path is not None:
                update_kwargs['path'] = payload.path
            if payload.component is not None:
                update_kwargs['component'] = payload.component
            if payload.is_active is not None:
                update_kwargs['is_active'] = payload.is_active
            if payload.method is not None:
                update_kwargs['method'] = payload.method
            if payload.parent_id is not None:
                update_kwargs['parent_id'] = payload.parent_id
            if payload.meta_id is not None:
                update_kwargs['meta_id'] = payload.meta_id
                
            menu_data = self.service.update_menu(
                menu_id=menu_id,
                **update_kwargs
            )
            return success(menu_data, "Menu updated successfully")
        except BusinessException as e:
            return error(str(e), 400)
        except Exception as e:
            return error(str(e), 400)

    @http_delete("/{menu_id}", response=ApiResponse[None])
    def delete_menu(self, menu_id: str):
        try:
            self.service.delete_menu(menu_id)
            return success(None, "Menu deleted successfully")
        except BusinessException as e:
            return error(str(e), 400)
        except Exception as e:
            return error(str(e), 400)