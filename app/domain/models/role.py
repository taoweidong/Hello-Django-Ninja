"""
角色领域模型
"""

from django.db import models
from django.utils import timezone
from .user import User
import uuid


def generate_role_id():
    return uuid.uuid4().hex[:32]


class Role(models.Model):
    id = models.CharField(max_length=32, primary_key=True, default=generate_role_id)
    created_time = models.DateTimeField(default=timezone.now)
    updated_time = models.DateTimeField(default=timezone.now)
    description = models.CharField(max_length=256, null=True, blank=True)
    name = models.CharField(max_length=128, unique=True)
    code = models.CharField(max_length=128, unique=True, default="")
    is_active = models.BooleanField(default=True)
    
    # 外键关系
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_roles')
    modifier = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='modified_roles')
    
    class Meta:
        db_table = 'system_userrole'
        app_label = 'domain'

    def __str__(self) -> str:
        return str(self.name)