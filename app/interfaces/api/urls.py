"""
API 路由配置
"""

from ninja_extra import NinjaExtraAPI
from app.interfaces.api.controllers.auth import AuthController
from app.interfaces.api.controllers.users import UsersController
from app.interfaces.api.controllers.roles import RolesController
from app.interfaces.api.controllers.permissions import PermissionsController
from app.interfaces.api.controllers.health import HealthController
from ninja_jwt.authentication import JWTAuth


# 创建 API 实例，添加更多元数据和配置
api = NinjaExtraAPI(
    title="RBAC API",
    version="1.0.0",
    description="基于角色的访问控制(RBAC)系统API",
    openapi_url="/openapi.json",
    docs_url="/docs",
    auth=JWTAuth()  # 使用JWT认证
)

# 注册控制器
api.register_controllers(
    AuthController,
    UsersController,
    RolesController,
    PermissionsController,
    HealthController,
)