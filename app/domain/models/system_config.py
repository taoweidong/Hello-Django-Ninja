"""
系统配置领域模型
"""

from django.db import models

from .base_model import BaseModel


class SystemConfig(BaseModel):
    key = models.CharField(max_length=128, unique=True)
    value = models.TextField()
    status = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    access = models.BooleanField(default=True)
    inherit = models.BooleanField(default=True)
    
    def __str__(self) -> str:
        return f"SystemConfig {self.key}"
    
    class Meta(BaseModel.Meta):
        db_table = 'system_config'
        app_label = 'domain'