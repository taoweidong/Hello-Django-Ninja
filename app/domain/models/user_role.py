"""
用户角色关联领域模型
"""

from django.db import models

from .base_model import BaseModel


class UserRole(BaseModel):
    # 外键关系
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='user_roles')
    role = models.ForeignKey('Role', on_delete=models.CASCADE, related_name='user_roles')

    def __str__(self) -> str:
        return f"UserRole {self.user} - {self.role}"

    class Meta:
        db_table = 'system_user_role'
        app_label = 'domain'
