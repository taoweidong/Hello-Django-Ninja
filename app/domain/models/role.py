"""
角色领域模型
"""

import uuid

from django.db import models

from .base_model import BaseModel, generate_uuid_pk


def generate_role_id():
    return str(uuid.uuid4()).replace('-', '')


class Role(BaseModel):
    id = models.CharField(max_length=32, primary_key=True, default=generate_uuid_pk)
    name = models.CharField(max_length=128, unique=True)
    code = models.CharField(max_length=128, unique=True, default="")
    is_active = models.BooleanField(default=models.NOT_PROVIDED)
    
    def __str__(self) -> str:
        return str(self.name)
    
    class Meta:
        db_table = 'system_role'
        app_label = 'domain'