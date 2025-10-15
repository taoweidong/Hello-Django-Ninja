"""
部门管理 API Controller
"""

from django.core.exceptions import ObjectDoesNotExist
from django.apps import apps
from ninja_extra import api_controller, http_get, http_post, http_put, http_delete, permissions
from ninja_jwt.authentication import JWTAuth

from app.api.schemas import DepartmentOut, DepartmentCreate, DepartmentUpdate


@api_controller("/departments", auth=JWTAuth())
class DepartmentsController:
    def __init__(self):
        # 获取实际的 Django 模型类
        self.DepartmentModel = apps.get_model("domain", "Department")

    @http_post("/", response={201: DepartmentOut})
    def create_department(self, payload: DepartmentCreate):
        try:
            department = self.DepartmentModel(
                name=payload.name,
                code=payload.code,
                description=payload.description,
                rank=payload.rank,
                auto_bind=payload.auto_bind,
                is_active=payload.is_active,
                mode_type=payload.mode_type,
                parent_id=payload.parent_id
            )
            department.save()
            return 201, department
        except Exception as e:
            return 400, {"message": str(e)}

    @http_get("/{department_id}", response=DepartmentOut)
    def get_department(self, department_id: str):
        try:
            department = self.DepartmentModel.objects.get(id=department_id)
            return department
        except ObjectDoesNotExist:
            return 404, {"message": "Department not found"}

    @http_get("/", response=list[DepartmentOut])
    def list_departments(self):
        departments = self.DepartmentModel.objects.all()
        return departments

    @http_put("/{department_id}", response=DepartmentOut)
    def update_department(self, department_id: str, payload: DepartmentUpdate):
        try:
            department = self.DepartmentModel.objects.get(id=department_id)
            if payload.name is not None:
                department.name = payload.name
            if payload.code is not None:
                department.code = payload.code
            if payload.description is not None:
                department.description = payload.description
            if payload.rank is not None:
                department.rank = payload.rank
            if payload.auto_bind is not None:
                department.auto_bind = payload.auto_bind
            if payload.is_active is not None:
                department.is_active = payload.is_active
            if payload.mode_type is not None:
                department.mode_type = payload.mode_type
            if payload.parent_id is not None:
                department.parent_id = payload.parent_id
            department.save()
            return department
        except ObjectDoesNotExist:
            return 404, {"message": "Department not found"}
        except Exception as e:
            return 400, {"message": str(e)}

    @http_delete("/{department_id}", response={204: None})
    def delete_department(self, department_id: str):
        try:
            department = self.DepartmentModel.objects.get(id=department_id)
            department.delete()
            return 204, None
        except ObjectDoesNotExist:
            return 404, {"message": "Department not found"}