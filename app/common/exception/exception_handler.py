# exception_handler.py

from abc import ABC, abstractmethod
from typing import Dict, Type, Any
from functools import wraps

from loguru import logger
from ninja_extra import ControllerBase

from app.common.api_response import error


# ----------------------------
# 异常处理器策略基类
# ----------------------------
class ExceptionHandlerStrategy(ABC):
    @abstractmethod
    def handle(self, controller: ControllerBase, exc: Exception):
        pass


# ----------------------------
# 默认业务异常处理器（通用）
# ----------------------------
class DefaultBusinessExceptionHandler(ExceptionHandlerStrategy):
    def __init__(self, status_code: int = 400):
        self.status_code = status_code

    def handle(self, controller: ControllerBase, exc: Exception):
        logger.warning(f"业务异常: {exc} (code={self.status_code})")
        return controller.create_response(
            error(str(exc), self.status_code),
            status_code=self.status_code
        )


# ----------------------------
# 全局注册中心
# ----------------------------
class ExceptionHandlerRegistry:
    _handlers: Dict[Type[Exception], ExceptionHandlerStrategy] = {}

    @classmethod
    def register(cls, exc_type: Type[Exception], handler: ExceptionHandlerStrategy):
        cls._handlers[exc_type] = handler

    @classmethod
    def get_handler(cls, exc: Exception) -> ExceptionHandlerStrategy | None:
        for exc_type in cls._handlers:
            if isinstance(exc, exc_type):
                return cls._handlers[exc_type]
        return None


# ----------------------------
# 自动注册装饰器
# ----------------------------
def register_exception_handler(cls: Type[Exception]) -> Type[Exception]:
    """
    装饰器：用于在定义异常类时自动注册默认处理器。
    要求异常类定义 status_code 属性。
    """
    if not hasattr(cls, 'status_code'):
        raise TypeError(f"异常类 {cls.__name__} 必须定义 status_code 属性")

    handler = DefaultBusinessExceptionHandler(status_code=cls.status_code)
    ExceptionHandlerRegistry.register(cls, handler)
    return cls


# ----------------------------
# 其他特殊异常处理器（如需要自定义逻辑）
# ----------------------------
# 示例：如果某个异常需要特殊处理（比如记录审计日志），可单独定义
# @ExceptionHandlerRegistry.register(SomeSpecialException)
# class SpecialHandler(ExceptionHandlerStrategy): ...


# ----------------------------
# 全局异常入口
# ----------------------------
def global_exception_handler(controller: ControllerBase, exc: Exception):
    logger.exception(f"全局异常处理器捕获到异常: {exc}")

    handler = ExceptionHandlerRegistry.get_handler(exc)
    if handler:
        return handler.handle(controller, exc)

    # 未注册的异常（如系统异常）
    logger.error("未预期的异常类型，返回 500")
    return controller.create_response(
        error("Internal server error", 500),
        status_code=500
    )