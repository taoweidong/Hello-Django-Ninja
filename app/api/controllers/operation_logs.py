"""
操作日志管理 API Controller
"""

from django.core.exceptions import ObjectDoesNotExist
from django.apps import apps
from ninja_extra import api_controller, http_get, http_post, http_put, http_delete, permissions
from ninja_jwt.authentication import JWTAuth

from app.api.schemas import OperationLogOut, OperationLogCreate, OperationLogUpdate


@api_controller("/operation-logs", auth=JWTAuth())
class OperationLogsController:
    def __init__(self):
        # 获取实际的 Django 模型类
        self.OperationLogModel = apps.get_model("domain", "OperationLog")

    @http_post("/", response={201: OperationLogOut})
    def create_operation_log(self, payload: OperationLogCreate):
        try:
            operation_log = self.OperationLogModel(
                module=payload.module,
                path=payload.path,
                body=payload.body,
                method=payload.method,
                ipaddress=payload.ipaddress,
                browser=payload.browser,
                system=payload.system,
                response_code=payload.response_code,
                response_result=payload.response_result,
                status_code=payload.status_code,
                creator_id=payload.creator_id,
                modifier_id=payload.modifier_id
            )
            operation_log.save()
            return 201, operation_log
        except Exception as e:
            return 400, {"message": str(e)}

    @http_get("/{operation_log_id}", response=OperationLogOut)
    def get_operation_log(self, operation_log_id: int):
        try:
            operation_log = self.OperationLogModel.objects.get(id=operation_log_id)
            return operation_log
        except ObjectDoesNotExist:
            return 404, {"message": "OperationLog not found"}

    @http_get("/", response=list[OperationLogOut])
    def list_operation_logs(self):
        operation_logs = self.OperationLogModel.objects.all()
        return operation_logs

    @http_put("/{operation_log_id}", response=OperationLogOut)
    def update_operation_log(self, operation_log_id: int, payload: OperationLogUpdate):
        try:
            operation_log = self.OperationLogModel.objects.get(id=operation_log_id)
            if payload.module is not None:
                operation_log.module = payload.module
            if payload.path is not None:
                operation_log.path = payload.path
            if payload.body is not None:
                operation_log.body = payload.body
            if payload.method is not None:
                operation_log.method = payload.method
            if payload.ipaddress is not None:
                operation_log.ipaddress = payload.ipaddress
            if payload.browser is not None:
                operation_log.browser = payload.browser
            if payload.system is not None:
                operation_log.system = payload.system
            if payload.response_code is not None:
                operation_log.response_code = payload.response_code
            if payload.response_result is not None:
                operation_log.response_result = payload.response_result
            if payload.status_code is not None:
                operation_log.status_code = payload.status_code
            if payload.creator_id is not None:
                operation_log.creator_id = payload.creator_id
            if payload.modifier_id is not None:
                operation_log.modifier_id = payload.modifier_id
            operation_log.save()
            return operation_log
        except ObjectDoesNotExist:
            return 404, {"message": "OperationLog not found"}
        except Exception as e:
            return 400, {"message": str(e)}

    @http_delete("/{operation_log_id}", response={204: None})
    def delete_operation_log(self, operation_log_id: int):
        try:
            operation_log = self.OperationLogModel.objects.get(id=operation_log_id)
            operation_log.delete()
            return 204, None
        except ObjectDoesNotExist:
            return 404, {"message": "OperationLog not found"}