"""
健康检查 API Controller
"""

import sys
import platform
import socket
from datetime import datetime
from ninja_extra import api_controller, http_get
from ninja import Router
from django.db import connections
from django.db.utils import OperationalError
from django.http import HttpRequest
from app.interfaces.api.schemas import (
    HealthCheckSchema,
    SystemInfoSchema,
    DetailedHealthCheckSchema
)


@api_controller("/health")
class HealthController:
    """健康检查控制器"""
    
    @http_get("/", response=HealthCheckSchema)
    def health_check(self, request: HttpRequest):
        """基本健康检查接口"""
        return {
            "status": "healthy",
            "timestamp": datetime.now(),
            "service": "Hello-Django-Ninja",
            "version": "1.0.0"
        }
    
    @http_get("/detailed", response=DetailedHealthCheckSchema)
    def detailed_health_check(self, request: HttpRequest):
        """详细健康检查接口"""
        # 检查数据库连接
        db_status = self._check_database()
        
        # 获取系统信息
        system_info = self._get_system_info()
        
        # 获取依赖信息
        dependencies = self._get_dependencies()
        
        return {
            "status": "healthy" if db_status == "connected" else "unhealthy",
            "timestamp": datetime.now(),
            "service": "Hello-Django-Ninja",
            "version": "1.0.0",
            "system_info": system_info,
            "database_status": db_status,
            "dependencies": dependencies
        }
    
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
        return {
            "python_version": sys.version,
            "platform": platform.platform(),
            "hostname": socket.gethostname(),
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