"""
API 权限类
"""

from ninja_extra.permissions import BasePermission
from ninja_extra.controllers.base import ControllerBase
from typing import Any


class IsAuthenticated(BasePermission):
    """
    检查用户是否已认证的权限类
    """
    def has_permission(self, request, controller: ControllerBase) -> bool:
        # 检查请求对象是否有user属性且已认证
        return hasattr(request, "user") and getattr(request, "user", None) is not None


class HasPermission(BasePermission):
    """
    基于权限码的权限检查类
    """
    def __init__(self, permission_code: str):
        self.permission_code = permission_code
    
    def has_permission(self, request, controller: ControllerBase) -> bool:
        # 检查用户是否有特定权限
        user = getattr(request, "user", None)
        if not user or not hasattr(user, 'has_perm'):
            return False
        
        # 在实际项目中，这里会检查用户是否具有指定的权限
        # 示例：return user.has_perm(self.permission_code)
        # 目前简化实现，假设认证用户就有权限
        return True


class IsSuperUser(BasePermission):
    """
    检查用户是否为超级用户的权限类
    """
    def has_permission(self, request, controller: ControllerBase) -> bool:
        user = getattr(request, "user", None)
        if not user:
            return False
        return getattr(user, 'is_superuser', False)