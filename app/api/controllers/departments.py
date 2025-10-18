"""
部门管理 API Controller
"""

from ninja_extra import api_controller, http_get, http_post, http_put, http_delete
from ninja_jwt.authentication import JWTAuth

from app.application.services.department_service import DepartmentService
from app.common.exception.exceptions import BusinessException
from app.infrastructure.persistence.repos.department_repo_impl import DjangoORMDepartmentRepository
from app.api.schemas import DepartmentOut, DepartmentCreate, DepartmentUpdate, ApiResponse
from app.common.api_response import success, error


@api_controller("/departments", auth=JWTAuth())
class DepartmentsController:
    def __init__(self):
        # 实例化仓储实现
        department_repo = DjangoORMDepartmentRepository()
        # 实例化应用服务
        self.service = DepartmentService(department_repo)

    @http_post("/", response=ApiResponse[DepartmentOut])
    def create_department(self, payload: DepartmentCreate):
        try:
            department_data = self.service.create_department(
                name=payload.name,
                code=payload.code,
                description=payload.description,
                rank=payload.rank,
                auto_bind=payload.auto_bind,
                is_active=payload.is_active,
                mode_type=payload.mode_type,
                parent_id=payload.parent_id
            )
            return success(department_data, "Department created successfully", 201)
        except BusinessException as e:
            return error(str(e), 400)
        except Exception as e:
            return error(str(e), 400)

    @http_get("/{department_id}", response=ApiResponse[DepartmentOut])
    def get_department(self, department_id: str):
        try:
            department_data = self.service.get_department(department_id)
            return success(department_data, "Department retrieved successfully")
        except BusinessException as e:
            return error(str(e), 400)
        except Exception as e:
            return error(str(e), 400)

    @http_get("/", response=ApiResponse[list[DepartmentOut]])
    def list_departments(self):
        try:
            departments_data = self.service.list_departments()
            return success(departments_data, "Departments retrieved successfully")
        except Exception as e:
            return error(str(e), 400)

    @http_put("/{department_id}", response=ApiResponse[DepartmentOut])
    def update_department(self, department_id: str, payload: DepartmentUpdate):
        try:
            # 只传递非空值进行更新
            update_kwargs = {}
            if payload.name is not None:
                update_kwargs['name'] = payload.name
            if payload.code is not None:
                update_kwargs['code'] = payload.code
            if payload.description is not None:
                update_kwargs['description'] = payload.description
            if payload.rank is not None:
                update_kwargs['rank'] = payload.rank
            if payload.auto_bind is not None:
                update_kwargs['auto_bind'] = payload.auto_bind
            if payload.is_active is not None:
                update_kwargs['is_active'] = payload.is_active
            if payload.mode_type is not None:
                update_kwargs['mode_type'] = payload.mode_type
            if payload.parent_id is not None:
                update_kwargs['parent_id'] = payload.parent_id
                
            department_data = self.service.update_department(
                department_id=department_id,
                **update_kwargs
            )
            return success(department_data, "Department updated successfully")
        except BusinessException as e:
            return error(str(e), 400)
        except Exception as e:
            return error(str(e), 400)

    @http_delete("/{department_id}", response=ApiResponse[None])
    def delete_department(self, department_id: str):
        try:
            self.service.delete_department(department_id)
            return success(None, "Department deleted successfully")
        except BusinessException as e:
            return error(str(e), 400)
        except Exception as e:
            return error(str(e), 400)