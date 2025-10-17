"""
用户角色关联领域模型
"""

from django.db import models


class UserRole(models.Model):
    id = models.CharField(max_length=32, primary_key=True)
    created_time = models.DateTimeField()
    updated_time = models.DateTimeField()
    
    # 外键关系
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='user_roles')
    role = models.ForeignKey('Role', on_delete=models.CASCADE, related_name='user_roles')
    
    class Meta:
        db_table = 'system_user_role'
        app_label = 'domain'
    
    def __str__(self) -> str:
        return f"UserRole {self.user} - {self.role}"