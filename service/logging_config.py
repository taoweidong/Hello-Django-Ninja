"""
日志配置文件
使用loguru库配置服务的执行日志，并替换Python标准logging模块
"""

import os
import sys
import logging
from loguru import logger
from pathlib import Path
from typing import Optional

# 定义日志目录
BASE_DIR = Path(__file__).resolve().parent.parent
LOGS_DIR = BASE_DIR / "logs"

# 确保日志目录存在
LOGS_DIR.mkdir(exist_ok=True)

# 移除默认的日志处理器
logger.remove()

# 配置不同级别的日志文件
logger.add(
    LOGS_DIR / "debug.log",
    level="DEBUG",
    rotation="100 MB",
    retention="10 days",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}",
    enqueue=True,
    backtrace=True,
    diagnose=True
)

logger.add(
    LOGS_DIR / "info.log",
    level="INFO",
    rotation="100 MB",
    retention="30 days",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}",
    enqueue=True
)

logger.add(
    LOGS_DIR / "warning.log",
    level="WARNING",
    rotation="100 MB",
    retention="60 days",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}",
    enqueue=True
)

logger.add(
    LOGS_DIR / "error.log",
    level="ERROR",
    rotation="100 MB",
    retention="90 days",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}",
    enqueue=True,
    backtrace=True,
    diagnose=True
)

# 配置控制台输出
logger.add(
    sink=sys.stderr,  # 正确配置控制台输出
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {message}",
    enqueue=True
)

# 替换标准logging模块
class InterceptHandler(logging.Handler):
    def emit(self, record):
        # 获取对应的loguru日志等级
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # 查找调用日志记录的原始函数
        frame = logging.currentframe()
        if frame is not None:
            frame = frame.f_back
        depth = 2
        while frame is not None and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())

# 将所有现有的logger处理器替换为InterceptHandler
logging.basicConfig(handlers=[InterceptHandler()], level=0)

# 导出配置好的logger
__all__ = ["logger"]