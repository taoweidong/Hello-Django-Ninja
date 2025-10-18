"""
系统配置领域模型
"""
import uuid

from django.db import models

from .base_model import BaseModel, generate_uuid_pk


class SystemConfig(BaseModel):
    id = models.CharField(max_length=32, primary_key=True, default=generate_uuid_pk)
    key = models.CharField(max_length=128, unique=True)
    value = models.TextField()
    status = models.BooleanField(default=models.NOT_PROVIDED)
    
    def __str__(self) -> str:
        return f"SystemConfig {self.key}"
    
    class Meta:
        db_table = 'system_config'
        app_label = 'domain'