"""
用户相关应用服务
"""

from app.domain.repositories.user_repository import UserRepository
from app.domain.models.user import User
from app.common.exception.exceptions import BusinessException
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

    def get_user(self, user_id: int) -> dict:
        """
        根据ID获取用户
        """
        user = self.user_repo.find_by_id(user_id)
        if not user:
            raise BusinessException(f"User with id '{user_id}' not found.")
        return {"id": user.id, "username": user.username, "email": user.email}

    def update_user(self, user_id: int, username: str = None, email: str = None, password: str = None) -> dict:
        """
        更新用户信息
        """
        user = self.user_repo.find_by_id(user_id)
        if not user:
            raise BusinessException(f"User with id '{user_id}' not found.")
        
        if username is not None:
            user.username = username
        if email is not None:
            user.email = email
        if password is not None:
            user.set_password(password)
        
        self.user_repo.save(user)
        return {"id": user.id, "username": user.username, "email": user.email}

    def delete_user(self, user_id: int) -> bool:
        """
        删除用户
        """
        result = self.user_repo.delete(user_id)
        if not result:
            raise BusinessException(f"User with id '{user_id}' not found.")
        return result

    def list_users(self) -> List[dict]:
        """
        获取所有用户列表
        """
        users = self.user_repo.list_all()
        return [{"id": user.id, "username": user.username, "email": user.email} for user in users]

    def assign_role_to_user(self, user_id: int, role_id: int) -> None:
        """
        为用户分配角色
        """
        # 业务逻辑校验
        pass  # 简化实现