"""
菜单领域模型
"""

from django.db import models
from .base_model import BaseModel


class Menu(BaseModel):
    id = models.CharField(max_length=32, primary_key=True)
    name = models.CharField(max_length=128)
    code = models.CharField(max_length=128, unique=True)
    icon = models.CharField(max_length=100, null=True, blank=True)
    path = models.CharField(max_length=255, null=True, blank=True)
    component = models.CharField(max_length=255, null=True, blank=True)
    redirect = models.CharField(max_length=255, null=True, blank=True)
    hidden = models.BooleanField(default=models.NOT_PROVIDED)
    cache = models.BooleanField(default=models.NOT_PROVIDED)
    sort = models.IntegerField(default=models.NOT_PROVIDED)
    status = models.BooleanField(default=models.NOT_PROVIDED)
    remark = models.TextField(null=True, blank=True)
    
    # 外键关系
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')
    
    def __str__(self) -> str:
        return str(self.name)
    
    class Meta:
        db_table = 'system_menu'
        app_label = 'domain'