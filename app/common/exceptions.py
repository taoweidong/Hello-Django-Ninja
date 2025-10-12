"""
全局自定义异常定义
"""


class BusinessException(Exception):
    """业务异常基类"""

    pass


class NotFoundException(BusinessException):
    """未找到异常"""

    pass


class ValidationException(BusinessException):
    """验证异常"""

    pass


class PermissionDeniedException(BusinessException):
    """权限拒绝异常"""

    pass


class InvalidRoleAssignmentException(BusinessException):
    """无效角色分配异常"""

    pass
