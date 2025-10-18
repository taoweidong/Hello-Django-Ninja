"""
用户登录日志管理 API Controller
"""

from ninja_extra import api_controller, http_get, http_post, http_put, http_delete
from ninja_jwt.authentication import JWTAuth

from app.api.schemas import LoginLogOut, LoginLogCreate, LoginLogUpdate, ApiResponse
from app.application.services.login_log_service import LoginLogService
from app.common.api_response import success, error
from app.common.exception.exceptions import BusinessException
from app.infrastructure.persistence.repos.login_log_repo_impl import DjangoORMLoginLogRepository
from app.infrastructure.persistence.repos.user_repo_impl import DjangoORMUserRepository


@api_controller("/login-logs", auth=JWTAuth())
class LoginLogsController:
    def __init__(self):
        # 实例化仓储实现
        login_log_repo = DjangoORMLoginLogRepository()
        user_repo = DjangoORMUserRepository()
        # 实例化应用服务
        self.service = LoginLogService(login_log_repo, user_repo)

    @http_post("/", response=ApiResponse[LoginLogOut])
    def create_login_log(self, request, payload: LoginLogCreate):
        current_user = request.user  # 获取当前登录用户对象
        try:
            log_data = self.service.create_login_log(
                status=payload.status,
                login_type=payload.login_type,
                ipaddress=payload.ipaddress,
                browser=payload.browser,
                system=payload.system,
                agent=payload.agent,
                creator=current_user.username,  # 使用用户ID而不是用户名
            )
            return success(log_data, "Login log created successfully", 201)
        except BusinessException as e:
            return error(str(e), 400)
        except Exception as e:
            return error(str(e), 400)

    @http_get("/{login_log_id}", response=ApiResponse[LoginLogOut])
    def get_login_log(self, request, login_log_id: int):
        # 如果需要基于用户权限控制访问，可以在这里检查
        current_user = request.user
        try:
            log_data = self.service.get_login_log(login_log_id)
            return success(log_data, "Login log retrieved successfully")
        except BusinessException as e:
            return error(str(e), 400)
        except Exception as e:
            return error(str(e), 400)

    @http_get("/", response=ApiResponse[list[LoginLogOut]])
    def list_login_logs(self, request):
        # 如果需要基于用户权限过滤结果，可以在这里处理
        current_user = request.user
        try:
            logs_data = self.service.list_login_logs()
            return success(logs_data, "Login logs retrieved successfully")
        except Exception as e:
            return error(str(e), 400)

    @http_put("/{login_log_id}", response=ApiResponse[LoginLogOut])
    def update_login_log(self, request, login_log_id: int, payload: LoginLogUpdate):
        current_user = request.user
        try:
            # 只传递非空值进行更新
            update_kwargs = {}
            if payload.status is not None:
                update_kwargs['status'] = payload.status
            if payload.login_type is not None:
                update_kwargs['login_type'] = payload.login_type
            if payload.ipaddress is not None:
                update_kwargs['ipaddress'] = payload.ipaddress
            if payload.browser is not None:
                update_kwargs['browser'] = payload.browser
            if payload.system is not None:
                update_kwargs['system'] = payload.system
            if payload.agent is not None:
                update_kwargs['agent'] = payload.agent

            log_data = self.service.update_login_log(
                log_id=login_log_id,
                **update_kwargs
            )
            return success(log_data, "Login log updated successfully")
        except BusinessException as e:
            return error(str(e), 400)
        except Exception as e:
            return error(str(e), 400)

    @http_delete("/{login_log_id}", response=ApiResponse[None])
    def delete_login_log(self, request, login_log_id: int):
        current_user = request.user
        try:
            self.service.delete_login_log(login_log_id)
            return success(None, "Login log deleted successfully")
        except BusinessException as e:
            return error(str(e), 400)
        except Exception as e:
            return error(str(e), 400)
