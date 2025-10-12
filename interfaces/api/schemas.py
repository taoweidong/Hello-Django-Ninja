"""
API 输入输出 Schema (DTOs)
"""

from ninja import Schema
from typing import List


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
