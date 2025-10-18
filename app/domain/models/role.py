"""
角色领域模型
"""

from django.db import models

from .base_model import BaseModel


class Role(BaseModel):
    name = models.CharField(max_length=128, unique=True)
    code = models.CharField(max_length=128, unique=True, default="")
    is_active = models.BooleanField(default=models.NOT_PROVIDED)

    def __str__(self) -> str:
        return str(self.name)

    class Meta:
        db_table = 'system_role'
        app_label = 'domain'
