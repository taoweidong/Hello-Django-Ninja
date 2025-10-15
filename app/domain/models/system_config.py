"""
系统配置领域模型
"""

from django.db import models
from .user import User


class SystemConfig(models.Model):
    id = models.CharField(max_length=32, primary_key=True)
    created_time = models.DateTimeField()
    updated_time = models.DateTimeField()
    description = models.CharField(max_length=256, null=True, blank=True)
    value = models.TextField()
    is_active = models.BooleanField()
    access = models.BooleanField()
    key = models.CharField(max_length=255, unique=True)
    inherit = models.BooleanField()
    
    # 外键关系
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_configs')
    modifier = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='modified_configs')
    
    class Meta:
        db_table = 'system_config'
    
    def __str__(self) -> str:
        return str(self.key)