"""
部门相关应用服务
"""

from app.domain.models.department import Department
from app.domain.repositories.department_repository import DepartmentRepository
from app.common.exception.exceptions import BusinessException
from typing import List, Optional


class DepartmentService:
    def __init__(self, department_repo: DepartmentRepository):
        self.department_repo = department_repo

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
        if self.department_repo.find_by_code(code):
            raise BusinessException(f"Department with code '{code}' already exists.")
        
        # 如果提供了parent_id，验证父部门是否存在
        if parent_id is not None:
            parent_department = self.department_repo.find_by_id(parent_id)
            if not parent_department:
                raise BusinessException(f"Parent department with id '{parent_id}' not found.")
        
        department = Department(
            name=name,
            code=code,
            rank=rank,
            auto_bind=auto_bind,
            is_active=is_active,
            mode_type=mode_type
        )
        if description is not None:
            department.description = description  # type: ignore
        if parent_id is not None:
            department.parent_id = parent_id  # type: ignore
        self.department_repo.save(department)
        return self._department_to_dict(department)

    def get_department(self, department_id: str) -> dict:
        """
        根据ID获取部门
        """
        department = self.department_repo.find_by_id(department_id)
        if not department:
            raise BusinessException(f"Department with id '{department_id}' not found.")
        return self._department_to_dict(department)

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
        department = self.department_repo.find_by_id(department_id)
        if not department:
            raise BusinessException(f"Department with id '{department_id}' not found.")
        
        # 如果提供了parent_id，验证父部门是否存在
        if parent_id is not None and parent_id != "":
            parent_department = self.department_repo.find_by_id(parent_id)
            if not parent_department:
                raise BusinessException(f"Parent department with id '{parent_id}' not found.")
        
        if name is not None:
            department.name = name  # type: ignore
        if code is not None:
            # 检查code是否已存在（排除当前部门）
            existing_dept = self.department_repo.find_by_code(code)
            if existing_dept and existing_dept.id != department_id:
                raise BusinessException(f"Department with code '{code}' already exists.")
            department.code = code  # type: ignore
        if description is not None:
            department.description = description  # type: ignore
        if rank is not None:
            department.rank = rank  # type: ignore
        if auto_bind is not None:
            department.auto_bind = auto_bind  # type: ignore
        if is_active is not None:
            department.is_active = is_active  # type: ignore
        if mode_type is not None:
            department.mode_type = mode_type  # type: ignore
        if parent_id is not None:
            # 允许设置为空字符串来清除父部门关系
            if parent_id == "":
                department.parent_id = None  # type: ignore
            else:
                department.parent_id = parent_id  # type: ignore
        
        self.department_repo.save(department)
        return self._department_to_dict(department)

    def delete_department(self, department_id: str) -> bool:
        """
        删除部门
        """
        result = self.department_repo.delete(department_id)
        if not result:
            raise BusinessException(f"Department with id '{department_id}' not found.")
        return result

    def list_departments(self) -> List[dict]:
        """
        获取所有部门列表
        """
        departments = self.department_repo.list_all()
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
            "parent_id": getattr(department, 'parent_id', None),
            "created_time": department.created_time,
            "updated_time": department.updated_time
        }