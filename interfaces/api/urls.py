"""
API 路由配置
"""

from ninja_extra import NinjaExtraAPI
from interfaces.api.controllers.auth import AuthController
from interfaces.api.controllers.users import UsersController
from interfaces.api.controllers.roles import RolesController
from interfaces.api.controllers.permissions import PermissionsController


# 创建 API 实例
api = NinjaExtraAPI(title="RBAC API", version="1.0.0")

# 注册控制器
api.register_controllers(
    AuthController,
    UsersController,
    RolesController,
    PermissionsController,
)
