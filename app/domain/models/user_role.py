"""
用户角色关联模型
"""

from django.db import models
from .user import User
from .role import Role


class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'system_userinfo_roles'
        unique_together = ('user', 'role')
    
    def __str__(self) -> str:
        return f"{self.user} - {self.role}"