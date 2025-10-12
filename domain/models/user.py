"""
用户领域模型
"""

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
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

    @property
    def id(self) -> int:
        return self.pk
