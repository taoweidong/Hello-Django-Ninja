"""
菜单元数据管理 API Controller
"""

from ninja_extra import api_controller, http_get, http_post, http_put, http_delete
from ninja_jwt.authentication import JWTAuth

from app.application.services.menu_meta_service import MenuMetaService
from app.common.exception.exceptions import BusinessException
from app.api.schemas import MenuMetaOut, MenuMetaCreate, MenuMetaUpdate, ApiResponse
from app.common.api_response import success, error


@api_controller("/menu-metas", auth=JWTAuth())
class MenuMetasController:
    def __init__(self):
        # 实例化应用服务
        self.service = MenuMetaService()

    @http_post("/", response=ApiResponse[MenuMetaOut])
    def create_menu_meta(self, payload: MenuMetaCreate):
        try:
            menu_meta_data = self.service.create_menu_meta(
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
            return success(menu_meta_data, "Menu meta created successfully", 201)
        except BusinessException as e:
            return error(str(e), 400)
        except Exception as e:
            return error(str(e), 400)

    @http_get("/{menu_meta_id}", response=ApiResponse[MenuMetaOut])
    def get_menu_meta(self, menu_meta_id: str):
        try:
            menu_meta_data = self.service.get_menu_meta(menu_meta_id)
            return success(menu_meta_data, "Menu meta retrieved successfully")
        except BusinessException as e:
            return error(str(e), 400)
        except Exception as e:
            return error(str(e), 400)

    @http_get("/", response=ApiResponse[list[MenuMetaOut]])
    def list_menu_metas(self):
        try:
            menu_metas_data = self.service.list_menu_metas()
            return success(menu_metas_data, "Menu metas retrieved successfully")
        except Exception as e:
            return error(str(e), 400)

    @http_put("/{menu_meta_id}", response=ApiResponse[MenuMetaOut])
    def update_menu_meta(self, menu_meta_id: str, payload: MenuMetaUpdate):
        try:
            # 只传递非空值进行更新
            update_kwargs = {}
            if payload.title is not None:
                update_kwargs['title'] = payload.title
            if payload.icon is not None:
                update_kwargs['icon'] = payload.icon
            if payload.r_svg_name is not None:
                update_kwargs['r_svg_name'] = payload.r_svg_name
            if payload.is_show_menu is not None:
                update_kwargs['is_show_menu'] = payload.is_show_menu
            if payload.is_show_parent is not None:
                update_kwargs['is_show_parent'] = payload.is_show_parent
            if payload.is_keepalive is not None:
                update_kwargs['is_keepalive'] = payload.is_keepalive
            if payload.frame_url is not None:
                update_kwargs['frame_url'] = payload.frame_url
            if payload.frame_loading is not None:
                update_kwargs['frame_loading'] = payload.frame_loading
            if payload.transition_enter is not None:
                update_kwargs['transition_enter'] = payload.transition_enter
            if payload.transition_leave is not None:
                update_kwargs['transition_leave'] = payload.transition_leave
            if payload.is_hidden_tag is not None:
                update_kwargs['is_hidden_tag'] = payload.is_hidden_tag
            if payload.fixed_tag is not None:
                update_kwargs['fixed_tag'] = payload.fixed_tag
            if payload.dynamic_level is not None:
                update_kwargs['dynamic_level'] = payload.dynamic_level
                
            menu_meta_data = self.service.update_menu_meta(
                menu_meta_id=menu_meta_id,
                **update_kwargs
            )
            return success(menu_meta_data, "Menu meta updated successfully")
        except BusinessException as e:
            return error(str(e), 400)
        except Exception as e:
            return error(str(e), 400)

    @http_delete("/{menu_meta_id}", response=ApiResponse[None])
    def delete_menu_meta(self, menu_meta_id: str):
        try:
            self.service.delete_menu_meta(menu_meta_id)
            return success(None, "Menu meta deleted successfully")
        except BusinessException as e:
            return error(str(e), 400)
        except Exception as e:
            return error(str(e), 400)