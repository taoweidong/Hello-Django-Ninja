"""
统一API响应处理工具
"""

from datetime import datetime
from typing import Optional, TypeVar, Generic, Any
from app.api.schemas import ApiResponse


T = TypeVar('T')


def success(data: Optional[T] = None, message: str = "Success", code: int = 200) -> ApiResponse[T]:
    """成功响应"""
    return ApiResponse(
        code=code,
        message=message,
        data=data,
        timestamp=datetime.now()
    )


def error(message: str = "Error", code: int = 400, data: Optional[Any] = None) -> ApiResponse[Any]:
    """错误响应"""
    return ApiResponse(
        code=code,
        message=message,
        data=data,
        timestamp=datetime.now()
    )


def not_found(message: str = "Not Found", code: int = 404) -> ApiResponse[Any]:
    """未找到响应"""
    return ApiResponse(
        code=code,
        message=message,
        data=None,
        timestamp=datetime.now()
    )


def unauthorized(message: str = "Unauthorized", code: int = 401) -> ApiResponse[Any]:
    """未授权响应"""
    return ApiResponse(
        code=code,
        message=message,
        data=None,
        timestamp=datetime.now()
    )


def forbidden(message: str = "Forbidden", code: int = 403) -> ApiResponse[Any]:
    """禁止访问响应"""
    return ApiResponse(
        code=code,
        message=message,
        data=None,
        timestamp=datetime.now()
    )