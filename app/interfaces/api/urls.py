"""
API 路由配置
"""

from ninja_extra import NinjaExtraAPI
from app.interfaces.api.controllers.auth import AuthController
from app.interfaces.api.controllers.users import UsersController
from app.interfaces.api.controllers.roles import RolesController
from app.interfaces.api.controllers.permissions import PermissionsController
from app.interfaces.api.controllers.health import HealthController


# 创建 API 实例
api = NinjaExtraAPI(title="RBAC API", version="1.0.0")

# 注册控制器
api.register_controllers(
    AuthController,
    UsersController,
    RolesController,
    PermissionsController,
    HealthController,
)