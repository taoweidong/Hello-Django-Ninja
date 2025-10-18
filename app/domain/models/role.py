"""
角色领域模型
"""

from django.db import models
from django.utils import timezone
from .base_model import BaseModel
import uuid


def generate_role_id():
    return uuid.uuid4().hex[:32]


class Role(BaseModel):
    id = models.CharField(max_length=32, primary_key=True, default=generate_role_id)
    name = models.CharField(max_length=128, unique=True)
    code = models.CharField(max_length=128, unique=True, default="")
    is_active = models.BooleanField(default=models.NOT_PROVIDED)
    
    def __str__(self) -> str:
        return str(self.name)
    
    class Meta:
        db_table = 'system_userrole'
        app_label = 'domain'