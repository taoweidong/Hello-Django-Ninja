"""
用户领域模型
"""

from django.contrib.auth.models import AbstractUser
from django.db import models

from .base_model import BaseModel
from .department import Department


class User(BaseModel, AbstractUser):
    mode_type = models.SmallIntegerField(default=0)  # 添加默认值
    avatar = models.CharField(max_length=100, null=True, blank=True)
    nickname = models.CharField(max_length=150, default="")  # 添加默认值
    gender = models.IntegerField(default=0)  # 添加默认值
    phone = models.CharField(max_length=16, default="")  # 添加默认值
    email = models.CharField(max_length=254, default="")  # 添加默认值

    # 外键关系
    dept = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='users')

    # 添加 related_name 以避免与 Django 内置 User 模型冲突
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="domain_users",
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="domain_users",
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )

    def __str__(self) -> str:
        return str(self.username)

    class Meta(AbstractUser.Meta):
        db_table = 'system_user'
        app_label = 'domain'
