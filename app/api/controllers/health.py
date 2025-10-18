"""
健康检查 API Controller
"""

import platform
import socket
import sys
from datetime import datetime

import psutil
from django.db import connections
from django.db.utils import OperationalError
from django.http import HttpRequest
from ninja_extra import api_controller, http_get

from app.api.schemas import (
    HealthCheckSchema,
    DetailedHealthCheckSchema,
    ApiResponse
)
from app.common.api_response import success


@api_controller("/health", auth=None)
class HealthController:
    """健康检查控制器"""

    @http_get("/", response=ApiResponse[HealthCheckSchema])
    def health_check(self, request: HttpRequest):
        """基本健康检查接口"""
        health_data = {
            "status": "healthy",
            "timestamp": datetime.now(),
            "service": "Hello-Django-Ninja",
            "version": "1.0.0"
        }
        return success(health_data, "Health check successful")

    @http_get("/detailed", response=ApiResponse[DetailedHealthCheckSchema], auth=None)
    def detailed_health_check(self, request: HttpRequest):
        """详细健康检查接口"""
        # 检查数据库连接
        db_status = self._check_database()

        # 获取系统信息
        system_info = self._get_system_info()

        # 获取依赖信息
        dependencies = self._get_dependencies()

        detailed_data = {
            "status": "healthy" if db_status == "connected" else "unhealthy",
            "timestamp": datetime.now(),
            "service": "Hello-Django-Ninja",
            "version": "1.0.0",
            "system_info": system_info,
            "database_status": db_status,
            "dependencies": dependencies
        }
        return success(detailed_data, "Detailed health check successful")

    def _check_database(self) -> str:
        """检查数据库连接状态"""
        try:
            db_conn = connections['default']
            c = db_conn.cursor()
            return "connected"
        except (OperationalError, Exception):
            return "disconnected"

    def _get_system_info(self) -> dict:
        """获取系统信息"""
        # 获取内存信息
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')

        return {
            "python_version": sys.version,
            "platform": platform.platform(),
            "hostname": socket.gethostname(),
            "memory_total_gb": round(memory.total / (1024 ** 3), 2),
            "memory_available_gb": round(memory.available / (1024 ** 3), 2),
            "disk_total_gb": round(disk.total / (1024 ** 3), 2),
            "disk_free_gb": round(disk.free / (1024 ** 3), 2),
        }

    def _get_dependencies(self) -> dict:
        """获取依赖信息"""
        dependencies = {}
        try:
            import django
            dependencies["django"] = django.get_version()
        except ImportError:
            dependencies["django"] = "not installed"

        try:
            import ninja
            dependencies["django-ninja"] = getattr(ninja, '__version__', 'unknown')
        except ImportError:
            dependencies["django-ninja"] = "not installed"

        return dependencies
