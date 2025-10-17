"""
系统配置领域模型
"""

from django.db import models


class SystemConfig(models.Model):
    id = models.CharField(max_length=32, primary_key=True)
    created_time = models.DateTimeField()
    updated_time = models.DateTimeField()
    key = models.CharField(max_length=128, unique=True)
    value = models.TextField()
    description = models.CharField(max_length=256, null=True, blank=True)
    status = models.BooleanField(default=True)
    
    # 外键关系
    creator = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, blank=True, related_name='created_configs')
    modifier = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, blank=True, related_name='modified_configs')
    
    class Meta:
        db_table = 'system_config'
        app_label = 'domain'
    
    def __str__(self) -> str:
        return f"SystemConfig {self.key}"