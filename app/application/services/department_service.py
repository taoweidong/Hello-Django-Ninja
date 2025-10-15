"""
部门相关应用服务
"""

from app.domain.models.department import Department
from app.common.exceptions import BusinessException
from typing import List, Optional


class DepartmentService:
    def __init__(self):
        pass

    def create_department(
        self, 
        name: str, 
        code: str, 
        description: Optional[str] = None,
        rank: int = 0,
        auto_bind: bool = False,
        is_active: bool = True,
        mode_type: int = 0,
        parent_id: Optional[str] = None
    ) -> dict:
        """
        创建部门
        """
        # 检查code是否已存在
        if Department.objects.filter(code=code).exists():
            raise BusinessException(f"Department with code '{code}' already exists.")
        
        department = Department(
            name=name,
            code=code,
            description=description,
            rank=rank,
            auto_bind=auto_bind,
            is_active=is_active,
            mode_type=mode_type,
            parent_id=parent_id
        )
        department.save()
        return self._department_to_dict(department)

    def get_department(self, department_id: str) -> dict:
        """
        根据ID获取部门
        """
        try:
            department = Department.objects.get(id=department_id)
            return self._department_to_dict(department)
        except Department.DoesNotExist:
            raise BusinessException(f"Department with id '{department_id}' not found.")

    def update_department(
        self, 
        department_id: str, 
        name: Optional[str] = None,
        code: Optional[str] = None,
        description: Optional[str] = None,
        rank: Optional[int] = None,
        auto_bind: Optional[bool] = None,
        is_active: Optional[bool] = None,
        mode_type: Optional[int] = None,
        parent_id: Optional[str] = None
    ) -> dict:
        """
        更新部门信息
        """
        try:
            department = Department.objects.get(id=department_id)
            
            if name is not None:
                department.name = name
            if code is not None:
                # 检查code是否已存在（排除当前部门）
                if Department.objects.filter(code=code).exclude(id=department_id).exists():
                    raise BusinessException(f"Department with code '{code}' already exists.")
                department.code = code
            if description is not None:
                department.description = description
            if rank is not None:
                department.rank = rank
            if auto_bind is not None:
                department.auto_bind = auto_bind
            if is_active is not None:
                department.is_active = is_active
            if mode_type is not None:
                department.mode_type = mode_type
            if parent_id is not None:
                department.parent_id = parent_id
            
            department.save()
            return self._department_to_dict(department)
        except Department.DoesNotExist:
            raise BusinessException(f"Department with id '{department_id}' not found.")

    def delete_department(self, department_id: str) -> bool:
        """
        删除部门
        """
        try:
            department = Department.objects.get(id=department_id)
            department.delete()
            return True
        except Department.DoesNotExist:
            raise BusinessException(f"Department with id '{department_id}' not found.")

    def list_departments(self) -> List[dict]:
        """
        获取所有部门列表
        """
        departments = Department.objects.all()
        return [self._department_to_dict(dept) for dept in departments]

    def _department_to_dict(self, department: Department) -> dict:
        """
        将Department对象转换为字典
        """
        return {
            "id": department.id,
            "name": department.name,
            "code": department.code,
            "description": department.description,
            "rank": department.rank,
            "auto_bind": department.auto_bind,
            "is_active": department.is_active,
            "mode_type": department.mode_type,
            "parent_id": department.parent_id,
            "created_time": department.created_time,
            "updated_time": department.updated_time
        }