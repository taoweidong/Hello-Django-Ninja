"""
全局自定义异常定义 + 自动注册到异常处理中心
"""
from app.common.exception.exception_handler import register_exception_handler


class BusinessException(Exception):
    """业务异常基类"""
    status_code = 400


@register_exception_handler
class NotFoundException(BusinessException):
    """未找到异常"""
    status_code = 404


@register_exception_handler
class ValidationException(BusinessException):
    """验证异常"""
    status_code = 400


@register_exception_handler
class PermissionDeniedException(BusinessException):
    """权限拒绝异常"""
    status_code = 403


@register_exception_handler
class InvalidRoleAssignmentException(BusinessException):
    """无效角色分配异常"""
    status_code = 400
