"""
API 权限类
"""

from ninja.security import HttpBearer


class IsAuthenticated:
    def has_permission(self, request, *args, **kwargs):
        # 简化的权限检查
        return hasattr(request, "user") and request.user.is_authenticated
