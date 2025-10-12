"""
领域对象工厂
"""

from domain.models.user import User
from domain.models.role import Role
from django.contrib.auth.models import Permission


class UserFactory:
    @staticmethod
    def create_user(username: str, email: str, password: str) -> User:
        user = User(username=username, email=email)
        user.set_password(password)
        return user


class RoleFactory:
    @staticmethod
    def create_role(name: str, description: str = "") -> Role:
        return Role(name=name, description=description)


class PermissionFactory:
    @staticmethod
    def create_permission(name: str, codename: str, content_type) -> Permission:
        return Permission(name=name, codename=codename, content_type=content_type)
