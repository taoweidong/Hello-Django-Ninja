"""
应用层使用的 DTO 定义
"""

from typing import Optional, List


class UserDTO:
    def __init__(self, id: int, username: str, email: str):
        self.id = id
        self.username = username
        self.email = email


class RoleDTO:
    def __init__(self, id: int, name: str, description: str):
        self.id = id
        self.name = name
        self.description = description


class PermissionDTO:
    def __init__(self, id: int, name: str, codename: str):
        self.id = id
        self.name = name
        self.codename = codename
