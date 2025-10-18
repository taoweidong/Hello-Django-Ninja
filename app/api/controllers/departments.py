"""
部门管理 API Controller
"""

from ninja_extra import api_controller, http_get, http_post, http_put, http_delete
from ninja_jwt.authentication import JWTAuth

from app.application.services.department_service import DepartmentService
from app.common.exception.exceptions import BusinessException
from app.infrastructure.persistence.repos.department_repo_impl import DjangoORMDepartmentRepository
from app.api.schemas import DepartmentOut, DepartmentCreate, DepartmentUpdate


@api_controller("/departments", auth=JWTAuth())
class DepartmentsController:
    def __init__(self):
        # 实例化仓储实现
        department_repo = DjangoORMDepartmentRepository()
        # 实例化应用服务
        self.service = DepartmentService(department_repo)

    @http_post("/", response={201: DepartmentOut})
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
            return 201, department_data
        except BusinessException as e:
            return 400, {"message": str(e)}
        except Exception as e:
            return 400, {"message": str(e)}

    @http_get("/{department_id}", response=DepartmentOut)
    def get_department(self, department_id: str):
        try:
            department_data = self.service.get_department(department_id)
            return department_data
        except BusinessException as e:
            return 400, {"message": str(e)}
        except Exception as e:
            return 400, {"message": str(e)}

    @http_get("/", response=list[DepartmentOut])
    def list_departments(self):
        try:
            departments_data = self.service.list_departments()
            return departments_data
        except Exception as e:
            return 400, {"message": str(e)}

    @http_put("/{department_id}", response=DepartmentOut)
    def update_department(self, department_id: str, payload: DepartmentUpdate):
        try:
            department_data = self.service.update_department(
                department_id=department_id,
                name=payload.name,
                code=payload.code,
                description=payload.description,
                rank=payload.rank,
                auto_bind=payload.auto_bind,
                is_active=payload.is_active,
                mode_type=payload.mode_type,
                parent_id=payload.parent_id
            )
            return department_data
        except BusinessException as e:
            return 400, {"message": str(e)}
        except Exception as e:
            return 400, {"message": str(e)}

    @http_delete("/{department_id}", response={204: None})
    def delete_department(self, department_id: str):
        try:
            self.service.delete_department(department_id)
            return 204, None
        except BusinessException as e:
            return 400, {"message": str(e)}
        except Exception as e:
            return 400, {"message": str(e)}