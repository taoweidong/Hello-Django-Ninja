"""
用户相关应用服务
"""

from app.domain.repositories.user_repository import UserRepository
from app.domain.models.user import User
from app.common.exceptions import BusinessException
from typing import List


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def create_user(self, username: str, email: str, password: str) -> dict:
        """
        创建用户
        """
        if self.user_repo.find_by_username(username):
            raise BusinessException(f"User with username '{username}' already exists.")
        user = User(username=username, email=email)
        user.set_password(password)  # 设置密码哈希
        self.user_repo.save(user)
        return {"id": user.id, "username": user.username, "email": user.email}

    def assign_role_to_user(self, user_id: int, role_id: int) -> None:
        """
        为用户分配角色
        """
        # 业务逻辑校验
        pass  # 简化实现