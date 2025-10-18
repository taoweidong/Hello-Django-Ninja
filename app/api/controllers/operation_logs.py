"""
操作日志管理 API Controller
"""

from ninja_extra import api_controller, http_get, http_post, http_put, http_delete
from ninja_jwt.authentication import JWTAuth

from app.application.services.operation_log_service import OperationLogService
from app.common.exception.exceptions import BusinessException
from app.api.schemas import OperationLogOut, OperationLogCreate, OperationLogUpdate, ApiResponse
from app.common.api_response import success, error


@api_controller("/operation-logs", auth=JWTAuth())
class OperationLogsController:
    def __init__(self):
        # 实例化应用服务
        self.service = OperationLogService()

    @http_post("/", response=ApiResponse[OperationLogOut])
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
                creator_id=payload.creator_id
            )
            return success(log_data, "Operation log created successfully", 201)
        except BusinessException as e:
            return error(str(e), 400)
        except Exception as e:
            return error(str(e), 400)

    @http_get("/{operation_log_id}", response=ApiResponse[OperationLogOut])
    def get_operation_log(self, operation_log_id: int):
        try:
            log_data = self.service.get_operation_log(operation_log_id)
            return success(log_data, "Operation log retrieved successfully")
        except BusinessException as e:
            return error(str(e), 400)
        except Exception as e:
            return error(str(e), 400)

    @http_get("/", response=ApiResponse[list[OperationLogOut]])
    def list_operation_logs(self):
        try:
            logs_data = self.service.list_operation_logs()
            return success(logs_data, "Operation logs retrieved successfully")
        except Exception as e:
            return error(str(e), 400)

    @http_put("/{operation_log_id}", response=ApiResponse[OperationLogOut])
    def update_operation_log(self, operation_log_id: int, payload: OperationLogUpdate):
        try:
            # 只传递非空值进行更新
            update_kwargs = {}
            if payload.module is not None:
                update_kwargs['module'] = payload.module
            if payload.path is not None:
                update_kwargs['path'] = payload.path
            if payload.body is not None:
                update_kwargs['body'] = payload.body
            if payload.method is not None:
                update_kwargs['method'] = payload.method
            if payload.ipaddress is not None:
                update_kwargs['ipaddress'] = payload.ipaddress
            if payload.browser is not None:
                update_kwargs['browser'] = payload.browser
            if payload.system is not None:
                update_kwargs['system'] = payload.system
            if payload.response_code is not None:
                update_kwargs['response_code'] = payload.response_code
            if payload.response_result is not None:
                update_kwargs['response_result'] = payload.response_result
            if payload.status_code is not None:
                update_kwargs['status_code'] = payload.status_code
                
            log_data = self.service.update_operation_log(
                log_id=operation_log_id,
                **update_kwargs
            )
            return success(log_data, "Operation log updated successfully")
        except BusinessException as e:
            return error(str(e), 400)
        except Exception as e:
            return error(str(e), 400)

    @http_delete("/{operation_log_id}", response=ApiResponse[None])
    def delete_operation_log(self, operation_log_id: int):
        try:
            self.service.delete_operation_log(operation_log_id)
            return success(None, "Operation log deleted successfully")
        except BusinessException as e:
            return error(str(e), 400)
        except Exception as e:
            return error(str(e), 400)