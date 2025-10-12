"""
角色领域模型
"""

from django.db import models


class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    permissions = models.ManyToManyField("auth.Permission", blank=True)

    def __str__(self) -> str:
        return str(self.name)

    @property
    def id(self) -> int:
        return self.pk
