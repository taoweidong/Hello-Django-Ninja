"""
系统配置领域模型
"""

from django.db import models

from .base_model import BaseModel


class SystemConfig(BaseModel):
    key = models.CharField(max_length=128, unique=True)
    value = models.TextField()
    status = models.BooleanField(default=models.NOT_PROVIDED)
    
    def __str__(self) -> str:
        return f"SystemConfig {self.key}"
    
    class Meta:
        db_table = 'system_config'
        app_label = 'domain'