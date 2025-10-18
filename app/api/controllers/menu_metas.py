"""
菜单元数据管理 API Controller
"""

from ninja_extra import api_controller, http_get, http_post, http_put, http_delete
from ninja_jwt.authentication import JWTAuth

from app.application.services.menu_meta_service import MenuMetaService
from app.common.exception.exceptions import BusinessException
from app.api.schemas import MenuMetaOut, MenuMetaCreate, MenuMetaUpdate


@api_controller("/menu-metas", auth=JWTAuth())
class MenuMetasController:
    def __init__(self):
        # 实例化应用服务
        self.service = MenuMetaService()

    @http_post("/", response={201: MenuMetaOut})
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
            return 201, menu_meta_data
        except BusinessException as e:
            return 400, {"message": str(e)}
        except Exception as e:
            return 400, {"message": str(e)}

    @http_get("/{menu_meta_id}", response=MenuMetaOut)
    def get_menu_meta(self, menu_meta_id: str):
        try:
            menu_meta_data = self.service.get_menu_meta(menu_meta_id)
            return menu_meta_data
        except BusinessException as e:
            return 400, {"message": str(e)}
        except Exception as e:
            return 400, {"message": str(e)}

    @http_get("/", response=list[MenuMetaOut])
    def list_menu_metas(self):
        try:
            menu_metas_data = self.service.list_menu_metas()
            return menu_metas_data
        except Exception as e:
            return 400, {"message": str(e)}

    @http_put("/{menu_meta_id}", response=MenuMetaOut)
    def update_menu_meta(self, menu_meta_id: str, payload: MenuMetaUpdate):
        try:
            menu_meta_data = self.service.update_menu_meta(
                menu_meta_id=menu_meta_id,
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
            return menu_meta_data
        except BusinessException as e:
            return 400, {"message": str(e)}
        except Exception as e:
            return 400, {"message": str(e)}

    @http_delete("/{menu_meta_id}", response={204: None})
    def delete_menu_meta(self, menu_meta_id: str):
        try:
            self.service.delete_menu_meta(menu_meta_id)
            return 204, None
        except BusinessException as e:
            return 400, {"message": str(e)}
        except Exception as e:
            return 400, {"message": str(e)}