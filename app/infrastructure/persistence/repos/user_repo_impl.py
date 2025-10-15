"""
用户仓储实现
"""

from app.domain.repositories.user_repository import UserRepository
from app.domain.models.user import User
from django.core.exceptions import ObjectDoesNotExist
from typing import Optional, List
from django.apps import apps
from .base_repository import BaseRepository


class DjangoORMUserRepository(UserRepository, BaseRepository[User]):
    def __init__(self):
        # 获取实际的 Django 模型类
        self.UserModel = apps.get_model("domain", "User")
        # 初始化基类
        BaseRepository.__init__(self, self.UserModel)

    def save(self, user: User) -> None:
        user.save()

    def find_by_id(self, user_id: int) -> Optional[User]:
        try:
            return self.UserModel.objects.get(pk=user_id)
        except ObjectDoesNotExist:
            return None

    def find_by_username(self, username: str) -> Optional[User]:
        try:
            return self.UserModel.objects.get(username=username)
        except ObjectDoesNotExist:
            return None

    def delete(self, user_id: int) -> bool:
        try:
            user = self.UserModel.objects.get(pk=user_id)
            user.delete()
            return True
        except ObjectDoesNotExist:
            return False

    def list_all(self) -> List[User]:
        return list(self.UserModel.objects.all())