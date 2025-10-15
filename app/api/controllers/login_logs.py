"""
用户登录日志管理 API Controller
"""

from django.core.exceptions import ObjectDoesNotExist
from django.apps import apps
from ninja_extra import api_controller, http_get, http_post, http_put, http_delete, permissions
from ninja_jwt.authentication import JWTAuth

from app.api.schemas import LoginLogOut, LoginLogCreate, LoginLogUpdate


@api_controller("/login-logs", auth=JWTAuth())
class LoginLogsController:
    def __init__(self):
        # 获取实际的 Django 模型类
        self.LoginLogModel = apps.get_model("domain", "LoginLog")

    @http_post("/", response={201: LoginLogOut})
    def create_login_log(self, payload: LoginLogCreate):
        try:
            login_log = self.LoginLogModel(
                status=payload.status,
                ipaddress=payload.ipaddress,
                browser=payload.browser,
                system=payload.system,
                agent=payload.agent,
                login_type=payload.login_type,
                creator_id=payload.creator_id,
                modifier_id=payload.modifier_id
            )
            login_log.save()
            return 201, login_log
        except Exception as e:
            return 400, {"message": str(e)}

    @http_get("/{login_log_id}", response=LoginLogOut)
    def get_login_log(self, login_log_id: int):
        try:
            login_log = self.LoginLogModel.objects.get(id=login_log_id)
            return login_log
        except ObjectDoesNotExist:
            return 404, {"message": "LoginLog not found"}

    @http_get("/", response=list[LoginLogOut])
    def list_login_logs(self):
        login_logs = self.LoginLogModel.objects.all()
        return login_logs

    @http_put("/{login_log_id}", response=LoginLogOut)
    def update_login_log(self, login_log_id: int, payload: LoginLogUpdate):
        try:
            login_log = self.LoginLogModel.objects.get(id=login_log_id)
            if payload.status is not None:
                login_log.status = payload.status
            if payload.ipaddress is not None:
                login_log.ipaddress = payload.ipaddress
            if payload.browser is not None:
                login_log.browser = payload.browser
            if payload.system is not None:
                login_log.system = payload.system
            if payload.agent is not None:
                login_log.agent = payload.agent
            if payload.login_type is not None:
                login_log.login_type = payload.login_type
            if payload.creator_id is not None:
                login_log.creator_id = payload.creator_id
            if payload.modifier_id is not None:
                login_log.modifier_id = payload.modifier_id
            login_log.save()
            return login_log
        except ObjectDoesNotExist:
            return 404, {"message": "LoginLog not found"}
        except Exception as e:
            return 400, {"message": str(e)}

    @http_delete("/{login_log_id}", response={204: None})
    def delete_login_log(self, login_log_id: int):
        try:
            login_log = self.LoginLogModel.objects.get(id=login_log_id)
            login_log.delete()
            return 204, None
        except ObjectDoesNotExist:
            return 404, {"message": "LoginLog not found"}