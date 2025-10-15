"""
API 输入输出 Schema (DTOs)
"""

from ninja import Schema
from typing import List, Optional
from datetime import datetime


class RoleCreate(Schema):
    name: str
    description: str


class RoleOut(Schema):
    id: int
    name: str
    description: str


class PermissionOut(Schema):
    id: int
    name: str
    codename: str


class UserCreate(Schema):
    username: str
    email: str
    password: str


class UserOut(Schema):
    id: int
    username: str
    email: str


class HealthCheckSchema(Schema):
    """健康检查响应Schema"""
    status: str
    timestamp: datetime
    service: str
    version: str


class SystemInfoSchema(Schema):
    """系统信息Schema"""
    python_version: str
    platform: str
    hostname: str
    uptime: Optional[float] = None


class DetailedHealthCheckSchema(Schema):
    """详细健康检查响应Schema"""
    status: str
    timestamp: datetime
    service: str
    version: str
    system_info: SystemInfoSchema
    database_status: str
    dependencies: dict