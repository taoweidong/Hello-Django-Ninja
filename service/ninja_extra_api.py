"""
API 路由配置
"""
from loguru import logger
from ninja_extra import NinjaExtraAPI
from ninja_jwt.authentication import JWTAuth

from app.api.controllers.auth import AuthController
from app.api.controllers.health import HealthController
from app.api.controllers.permissions import PermissionsController
from app.api.controllers.roles import RolesController
from app.api.controllers.users import UsersController
from app.api.controllers.departments import DepartmentsController
from app.api.controllers.menus import MenusController
from app.api.controllers.menu_metas import MenuMetasController
from app.api.controllers.system_configs import SystemConfigsController
from app.api.controllers.login_logs import LoginLogsController
from app.api.controllers.operation_logs import OperationLogsController
from service import settings

# 创建 API 实例，添加更多元数据和配置
ninja_extra_api = NinjaExtraAPI(
    title="RBAC API",
    version="1.0.0",
    description="基于角色的访问控制(RBAC)系统API",
    openapi_url="/openapi.json",
    docs_url="/docs",
    auth=JWTAuth()  # 使用JWT认证
)

# 注册控制器
ninja_extra_api.register_controllers(
    AuthController,
    UsersController,
    RolesController,
    PermissionsController,
    HealthController,
    DepartmentsController,
    MenusController,
    MenuMetasController,
    SystemConfigsController,
    LoginLogsController,
    OperationLogsController,
)

# 打印完整的API文档地址
port = getattr(settings.settings, 'port', 8000)  # 默认使用8000端口
full_url = f"http://{settings.settings.allowed_hosts_list[0] if settings.settings.allowed_hosts_list else 'localhost'}:{port}/api{ninja_extra_api.docs_url}"
logger.info(f"Full API documentation available at: {full_url}")