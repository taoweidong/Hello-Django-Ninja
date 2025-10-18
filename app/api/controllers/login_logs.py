"""
用户登录日志管理 API Controller
"""

from ninja_extra import api_controller, http_get, http_post, http_put, http_delete
from ninja_jwt.authentication import JWTAuth

from app.application.services.login_log_service import LoginLogService
from app.common.exception.exceptions import BusinessException
from app.api.schemas import LoginLogOut, LoginLogCreate, LoginLogUpdate


@api_controller("/login-logs", auth=JWTAuth())
class LoginLogsController:
    def __init__(self):
        # 实例化应用服务
        self.service = LoginLogService()

    @http_post("/", response={201: LoginLogOut})
    def create_login_log(self, payload: LoginLogCreate):
        try:
            log_data = self.service.create_login_log(
                status=payload.status,
                login_type=payload.login_type,
                ipaddress=payload.ipaddress,
                browser=payload.browser,
                system=payload.system,
                agent=payload.agent,
                description=payload.description,
                creator_id=payload.creator_id
            )
            return 201, log_data
        except BusinessException as e:
            return 400, {"message": str(e)}
        except Exception as e:
            return 400, {"message": str(e)}

    @http_get("/{login_log_id}", response=LoginLogOut)
    def get_login_log(self, login_log_id: int):
        try:
            log_data = self.service.get_login_log(login_log_id)
            return log_data
        except BusinessException as e:
            return 400, {"message": str(e)}
        except Exception as e:
            return 400, {"message": str(e)}

    @http_get("/", response=list[LoginLogOut])
    def list_login_logs(self):
        try:
            logs_data = self.service.list_login_logs()
            return logs_data
        except Exception as e:
            return 400, {"message": str(e)}

    @http_put("/{login_log_id}", response=LoginLogOut)
    def update_login_log(self, login_log_id: int, payload: LoginLogUpdate):
        try:
            log_data = self.service.update_login_log(
                log_id=login_log_id,
                status=payload.status,
                login_type=payload.login_type,
                ipaddress=payload.ipaddress,
                browser=payload.browser,
                system=payload.system,
                agent=payload.agent,
                description=payload.description
            )
            return log_data
        except BusinessException as e:
            return 400, {"message": str(e)}
        except Exception as e:
            return 400, {"message": str(e)}

    @http_delete("/{login_log_id}", response={204: None})
    def delete_login_log(self, login_log_id: int):
        try:
            self.service.delete_login_log(login_log_id)
            return 204, None
        except BusinessException as e:
            return 400, {"message": str(e)}
        except Exception as e:
            return 400, {"message": str(e)}