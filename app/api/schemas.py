"""
API 输入输出 Schema (DTOs)
"""

from ninja import Schema
from typing import List, Optional, TypeVar, Generic
from datetime import datetime
from typing import TypeVar, Generic, Union


# 定义泛型类型变量
T = TypeVar('T')

class ApiResponse(Schema, Generic[T]):
    """统一API响应格式"""
    code: int
    message: str
    data: Optional[T] = None
    timestamp: datetime


class RoleCreate(Schema):
    name: str
    description: str


class RoleUpdate(Schema):
    name: Optional[str] = None
    description: Optional[str] = None


class RoleOut(Schema):
    id: str
    name: str
    description: str


class PermissionOut(Schema):
    id: int
    name: str
    codename: str


class PermissionCreate(Schema):
    name: str
    codename: str
    content_type_id: int


class PermissionUpdate(Schema):
    name: Optional[str] = None
    codename: Optional[str] = None
    content_type_id: Optional[int] = None


class UserCreate(Schema):
    username: str
    email: str
    password: str


class UserUpdate(Schema):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None


class UserOut(Schema):
    id: int
    username: str
    email: str


class DepartmentCreate(Schema):
    name: str
    code: str
    description: Optional[str] = None
    rank: int
    auto_bind: bool
    is_active: bool
    mode_type: int
    parent_id: Optional[str] = None


class DepartmentUpdate(Schema):
    name: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None
    rank: Optional[int] = None
    auto_bind: Optional[bool] = None
    is_active: Optional[bool] = None
    mode_type: Optional[int] = None
    parent_id: Optional[str] = None


class DepartmentOut(Schema):
    id: str
    created_time: datetime
    updated_time: datetime
    description: Optional[str] = None
    name: str
    code: str
    rank: int
    auto_bind: bool
    is_active: bool
    mode_type: int
    creator_id: Optional[int] = None
    modifier_id: Optional[int] = None
    parent_id: Optional[str] = None


class MenuCreate(Schema):
    menu_type: int
    name: str
    rank: int
    path: str
    component: Optional[str] = None
    is_active: bool
    method: Optional[str] = None
    parent_id: Optional[str] = None
    meta_id: str


class MenuUpdate(Schema):
    menu_type: Optional[int] = None
    name: Optional[str] = None
    rank: Optional[int] = None
    path: Optional[str] = None
    component: Optional[str] = None
    is_active: Optional[bool] = None
    method: Optional[str] = None
    parent_id: Optional[str] = None
    meta_id: Optional[str] = None


class MenuOut(Schema):
    id: str
    created_time: datetime
    updated_time: datetime
    description: Optional[str] = None
    menu_type: int
    name: str
    rank: int
    path: str
    component: Optional[str] = None
    is_active: bool
    method: Optional[str] = None
    creator_id: Optional[int] = None
    modifier_id: Optional[int] = None
    parent_id: Optional[str] = None
    meta_id: str


class MenuMetaCreate(Schema):
    title: Optional[str] = None
    icon: Optional[str] = None
    r_svg_name: Optional[str] = None
    is_show_menu: bool
    is_show_parent: bool
    is_keepalive: bool
    frame_url: Optional[str] = None
    frame_loading: bool
    transition_enter: Optional[str] = None
    transition_leave: Optional[str] = None
    is_hidden_tag: bool
    fixed_tag: bool
    dynamic_level: int


class MenuMetaUpdate(Schema):
    title: Optional[str] = None
    icon: Optional[str] = None
    r_svg_name: Optional[str] = None
    is_show_menu: Optional[bool] = None
    is_show_parent: Optional[bool] = None
    is_keepalive: Optional[bool] = None
    frame_url: Optional[str] = None
    frame_loading: Optional[bool] = None
    transition_enter: Optional[str] = None
    transition_leave: Optional[str] = None
    is_hidden_tag: Optional[bool] = None
    fixed_tag: Optional[bool] = None
    dynamic_level: Optional[int] = None


class MenuMetaOut(Schema):
    id: str
    created_time: datetime
    updated_time: datetime
    description: Optional[str] = None
    title: Optional[str] = None
    icon: Optional[str] = None
    r_svg_name: Optional[str] = None
    is_show_menu: bool
    is_show_parent: bool
    is_keepalive: bool
    frame_url: Optional[str] = None
    frame_loading: bool
    transition_enter: Optional[str] = None
    transition_leave: Optional[str] = None
    is_hidden_tag: bool
    fixed_tag: bool
    dynamic_level: int
    creator_id: Optional[int] = None
    modifier_id: Optional[int] = None


class SystemConfigCreate(Schema):
    key: str
    value: str
    description: Optional[str] = None
    is_active: bool
    access: bool
    inherit: bool


class SystemConfigUpdate(Schema):
    key: Optional[str] = None
    value: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    access: Optional[bool] = None
    inherit: Optional[bool] = None


class SystemConfigOut(Schema):
    id: str
    created_time: datetime
    updated_time: datetime
    description: Optional[str] = None
    value: str
    is_active: bool
    access: bool
    key: str
    inherit: bool
    creator_id: Optional[int] = None
    modifier_id: Optional[int] = None


class LoginLogCreate(Schema):
    status: bool
    ipaddress: Optional[str] = None
    browser: Optional[str] = None
    system: Optional[str] = None
    agent: Optional[str] = None
    login_type: int
    creator_id: Optional[int] = None
    modifier_id: Optional[int] = None


class LoginLogUpdate(Schema):
    status: Optional[bool] = None
    ipaddress: Optional[str] = None
    browser: Optional[str] = None
    system: Optional[str] = None
    agent: Optional[str] = None
    login_type: Optional[int] = None
    creator_id: Optional[int] = None
    modifier_id: Optional[int] = None


class LoginLogOut(Schema):
    id: int
    created_time: datetime
    updated_time: datetime
    description: Optional[str] = None
    status: bool
    ipaddress: Optional[str] = None
    browser: Optional[str] = None
    system: Optional[str] = None
    agent: Optional[str] = None
    login_type: int
    creator_id: Optional[int] = None
    modifier_id: Optional[int] = None


class OperationLogCreate(Schema):
    module: Optional[str] = None
    path: Optional[str] = None
    body: Optional[str] = None
    method: Optional[str] = None
    ipaddress: Optional[str] = None
    browser: Optional[str] = None
    system: Optional[str] = None
    response_code: Optional[int] = None
    response_result: Optional[str] = None
    status_code: Optional[int] = None
    creator_id: Optional[int] = None
    modifier_id: Optional[int] = None


class OperationLogUpdate(Schema):
    module: Optional[str] = None
    path: Optional[str] = None
    body: Optional[str] = None
    method: Optional[str] = None
    ipaddress: Optional[str] = None
    browser: Optional[str] = None
    system: Optional[str] = None
    response_code: Optional[int] = None
    response_result: Optional[str] = None
    status_code: Optional[int] = None
    creator_id: Optional[int] = None
    modifier_id: Optional[int] = None


class OperationLogOut(Schema):
    id: int
    created_time: datetime
    updated_time: datetime
    description: Optional[str] = None
    module: Optional[str] = None
    path: Optional[str] = None
    body: Optional[str] = None
    method: Optional[str] = None
    ipaddress: Optional[str] = None
    browser: Optional[str] = None
    system: Optional[str] = None
    response_code: Optional[int] = None
    response_result: Optional[str] = None
    status_code: Optional[int] = None
    creator_id: Optional[int] = None
    modifier_id: Optional[int] = None


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