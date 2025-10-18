"""
菜单元数据领域模型
"""

from django.db import models

from .base_model import BaseModel, generate_uuid_pk


class MenuMeta(BaseModel):
    id = models.CharField(max_length=32, primary_key=True, default=generate_uuid_pk)
    title = models.CharField(max_length=128)
    icon = models.CharField(max_length=100, null=True, blank=True)
    hidden = models.BooleanField(default=models.NOT_PROVIDED)
    cache = models.BooleanField(default=models.NOT_PROVIDED)
    sort = models.IntegerField(default=models.NOT_PROVIDED)
    status = models.BooleanField(default=models.NOT_PROVIDED)
    remark = models.TextField(null=True, blank=True)
    
    def __str__(self) -> str:
        return str(self.title)
    
    class Meta:
        db_table = 'system_menu_meta'
        app_label = 'domain'