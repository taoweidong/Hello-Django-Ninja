"""
操作日志管理 API Controller
"""

from ninja_extra import api_controller, http_get, http_post, http_put, http_delete
from ninja_jwt.authentication import JWTAuth

from app.application.services.operation_log_service import OperationLogService
from app.common.exception.exceptions import BusinessException
from app.api.schemas import OperationLogOut, OperationLogCreate, OperationLogUpdate


@api_controller("/operation-logs", auth=JWTAuth())
class OperationLogsController:
    def __init__(self):
        # 实例化应用服务
        self.service = OperationLogService()

    @http_post("/", response={201: OperationLogOut})
    def create_operation_log(self, payload: OperationLogCreate):
        try:
            log_data = self.service.create_operation_log(
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
                description=payload.description,
                creator_id=payload.creator_id
            )
            return 201, log_data
        except BusinessException as e:
            return 400, {"message": str(e)}
        except Exception as e:
            return 400, {"message": str(e)}

    @http_get("/{operation_log_id}", response=OperationLogOut)
    def get_operation_log(self, operation_log_id: int):
        try:
            log_data = self.service.get_operation_log(operation_log_id)
            return log_data
        except BusinessException as e:
            return 400, {"message": str(e)}
        except Exception as e:
            return 400, {"message": str(e)}

    @http_get("/", response=list[OperationLogOut])
    def list_operation_logs(self):
        try:
            logs_data = self.service.list_operation_logs()
            return logs_data
        except Exception as e:
            return 400, {"message": str(e)}

    @http_put("/{operation_log_id}", response=OperationLogOut)
    def update_operation_log(self, operation_log_id: int, payload: OperationLogUpdate):
        try:
            log_data = self.service.update_operation_log(
                log_id=operation_log_id,
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
                description=payload.description
            )
            return log_data
        except BusinessException as e:
            return 400, {"message": str(e)}
        except Exception as e:
            return 400, {"message": str(e)}

    @http_delete("/{operation_log_id}", response={204: None})
    def delete_operation_log(self, operation_log_id: int):
        try:
            self.service.delete_operation_log(operation_log_id)
            return 204, None
        except BusinessException as e:
            return 400, {"message": str(e)}
        except Exception as e:
            return 400, {"message": str(e)}